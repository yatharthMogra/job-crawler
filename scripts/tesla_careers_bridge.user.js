// ==UserScript==
// @name         Tesla Careers → Local Ingestion Bridge
// @namespace    careermatch.tesla.bridge
// @version      1.0
// @description  Pushes Tesla careers state + new job details to local ingestion pipeline
// @match        https://www.tesla.com/careers/search/*
// @grant        GM_xmlhttpRequest
// @connect      localhost
// @connect      127.0.0.1
// ==/UserScript==

(function () {
    'use strict';

    const INGEST_BASE = 'http://localhost:8000/ingest/tesla';
    const INGEST_TOKEN = ''; // optional: set to match TESLA_INGEST_TOKEN in job-ingestion .env
    const DETAIL_DELAY_MS = 300;
    const AUTO_RUN = true;
    const PAGE_READY_TIMEOUT_MS = 30000;

    function log(msg) {
        console.log(`[TeslaBridge] ${msg}`);
    }

    function gmRequest(method, url, body) {
        return new Promise((resolve, reject) => {
            const headers = { Accept: 'application/json' };
            if (INGEST_TOKEN) {
                headers['X-Ingest-Token'] = INGEST_TOKEN;
            }
            if (body !== undefined) {
                headers['Content-Type'] = 'application/json';
            }
            GM_xmlhttpRequest({
                method,
                url,
                headers,
                data: body !== undefined ? JSON.stringify(body) : undefined,
                onload(response) {
                    resolve({
                        ok: response.status >= 200 && response.status < 300,
                        status: response.status,
                        text: () => Promise.resolve(response.responseText),
                        json: () => Promise.resolve(JSON.parse(response.responseText)),
                    });
                },
                onerror: () => reject(new Error(`Request failed: ${method} ${url}`)),
            });
        });
    }

    async function waitForPageReady() {
        const deadline = Date.now() + PAGE_READY_TIMEOUT_MS;
        while (Date.now() < deadline) {
            const title = document.title;
            const hasResults = document.body?.innerText?.includes('Results');
            const hasJobLinks = document.querySelector('a[href*="/careers/search/job/"]');
            if (title === 'Tesla Careers' && (hasResults || hasJobLinks)) {
                return;
            }
            await new Promise((r) => setTimeout(r, 1000));
        }
        throw new Error('Tesla careers page did not become ready in time');
    }

    async function runBridge() {
        log('Waiting for page to be ready...');
        await waitForPageReady();

        log('Fetching state from Tesla API...');
        const stateResp = await fetch('/cua-api/apps/careers/state', {
            headers: { Accept: 'application/json' },
        });
        if (!stateResp.ok) {
            throw new Error(`State fetch failed: ${stateResp.status}`);
        }
        const stateData = await stateResp.json();
        if (!stateData || !Array.isArray(stateData.listings)) {
            throw new Error('Unexpected state shape: missing listings array');
        }
        log(`State returned ${stateData.listings.length} global listings.`);

        log('Requesting push plan from local server...');
        const planResp = await gmRequest('POST', `${INGEST_BASE}/plan`, { state: stateData });
        if (!planResp.ok) {
            throw new Error(
                `Plan request failed (${planResp.status}). Is job-ingestion running on localhost:8000?`
            );
        }
        const plan = await planResp.json();
        const pendingIds = plan.pending_detail_ids || [];
        log(
            `Plan: ${plan.listing_count} site listings (${(plan.sites || []).join(', ')}), ` +
                `${plan.known_count} known, ${pendingIds.length} need detail fetch.`
        );

        const details = [];
        for (let i = 0; i < pendingIds.length; i++) {
            const jobId = pendingIds[i];
            try {
                const detailResp = await fetch(`/cua-api/careers/job/${jobId}`, {
                    headers: { Accept: 'application/json' },
                });
                if (detailResp.ok) {
                    details.push(await detailResp.json());
                } else {
                    log(`Detail fetch failed for ${jobId}: HTTP ${detailResp.status}`);
                }
            } catch (err) {
                log(`Detail fetch failed for ${jobId}: ${err}`);
            }
            if (i % 25 === 0) {
                log(`Detail progress: ${i}/${pendingIds.length}`);
            }
            await new Promise((r) => setTimeout(r, DETAIL_DELAY_MS));
        }

        log(`Fetched ${details.length} details. Pushing to local server...`);
        const pushResp = await gmRequest('POST', `${INGEST_BASE}/push`, {
            state: stateData,
            details,
        });
        if (!pushResp.ok) {
            const body = await pushResp.text();
            throw new Error(`Push failed (${pushResp.status}): ${body.slice(0, 200)}`);
        }
        const result = await pushResp.json();
        log(`Push succeeded: ${JSON.stringify(result)}`);
        alert(
            `Tesla bridge done: ${result.listing_count} listings, ` +
                `${result.new_details_received} new details, ` +
                `${result.jobs_new} new / ${result.jobs_updated} updated.`
        );
    }

    function injectButton() {
        if (document.getElementById('tesla-bridge-btn')) {
            return;
        }
        const btn = document.createElement('button');
        btn.id = 'tesla-bridge-btn';
        btn.textContent = 'Push to ingestion';
        btn.style.cssText =
            'position:fixed;bottom:24px;right:24px;z-index:99999;padding:12px 16px;' +
            'background:#171a20;color:#fff;border:none;border-radius:4px;cursor:pointer;' +
            'font:14px system-ui,sans-serif;box-shadow:0 2px 8px rgba(0,0,0,.25);';
        btn.addEventListener('click', () => {
            btn.disabled = true;
            runBridge()
                .catch((err) => {
                    log(`Error: ${err}`);
                    alert(`Tesla bridge failed: ${err}`);
                })
                .finally(() => {
                    btn.disabled = false;
                });
        });
        document.body.appendChild(btn);
    }

    injectButton();
    if (AUTO_RUN) {
        runBridge().catch((err) => {
            log(`Auto-run error: ${err}`);
        });
    }
})();
