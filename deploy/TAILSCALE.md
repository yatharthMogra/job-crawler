# Tailscale — home machine access

The Linux home machine is reachable over [Tailscale](https://tailscale.com) from your Mac **at home or away** (no LAN IP, no router port forwarding). SSH and the remote-ops tunnel scripts use this path by default.

## Home machine

| Field | Value |
|-------|-------|
| **Tailscale IPv4** | `100.111.129.27` |
| **Linux user** | `ram` |
| **SSH alias** | `job-crawler-home` (in `~/.ssh/config`) |
| **Hostname** | `ram-Nitro-AN715-51` (MagicDNS, if enabled in Tailscale admin) |

If the IP ever changes (device removed and re-added to Tailscale), on Linux run:

```bash
tailscale ip -4
```

Update `HostName` in `~/.ssh/config` and `HOME_TAILSCALE_IP` in `deploy/home-remote.env`.

## One-time setup

### Linux (home machine)

```bash
# Install: https://tailscale.com/download/linux
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
sudo systemctl enable tailscaled

tailscale ip -4   # should include 100.111.129.27
```

### Mac (dev machine)

1. Install Tailscale from [tailscale.com/download](https://tailscale.com/download) and sign in with the **same account** as Linux.
2. Confirm you can reach the home machine:

   ```bash
   ping -c 2 100.111.129.27
   ssh ram@100.111.129.27 'echo ok'
   ```

3. SSH key + config — see [`deploy/ssh/config.example`](ssh/config.example). Append the `Host job-crawler-home` block to `~/.ssh/config`.
4. Copy remote ops config:

   ```bash
   cp deploy/home-remote.env.example deploy/home-remote.env
   ```

## Daily remote ops (Mac)

Tailscale must be connected on both machines. Then:

```bash
# Terminal 1 — keep open
./scripts/tunnel-home-services.sh

# Terminal 2
./scripts/home-health.sh
./scripts/dev-ingestion-dashboard.sh
```

Direct SSH (no tunnel) for logs or shell:

```bash
ssh job-crawler-home 'sudo journalctl -u job-ingestion -f'
```

## Security

- Do **not** expose job ingestion port `8000` or the notification worker on the public internet.
- Access APIs via SSH `LocalForward` (tunnel scripts) or Tailscale SSH only.
- The ingestion API has no authentication; Tailscale + SSH keys are the access boundary.

## Cursor IDE

If SSH fails in Cursor’s terminal with `No route to host` but works in Terminal.app, grant **Local Network** permission to Cursor (System Settings → Privacy & Security → Local Network), or run `./scripts/tunnel-home-services.sh` in Terminal.app and use Cursor only for `localhost` API calls.

## Related

- [`deploy/ssh/config.example`](ssh/config.example) — SSH host + port forwards
- [`DEPLOYMENT.md`](../DEPLOYMENT.md) Phase 6.9 — full remote ops workflow
