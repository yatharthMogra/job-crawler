# JD Structuring: Implementation Guide for Tiers 2–4

## Scope of this document

This picks up from the problem/options doc and goes one level deeper on the three tiers that do the real work in the deterministic pipeline:

- **Tier 2** — HTML DOM parsing (structure survives, no LLM)
- **Tier 3** — Header lexicon on preserved text (synonym + fuzzy matching)
- **Tier 4** — Small classifier for the long tail (not generative)

Tier 1 (platform-native mapping) and Tier 5 (heuristic fallback) are intentionally out of scope here — they're either mostly config (Tier 1) or a two-line fallback (Tier 5). This doc assumes the target output is the canonical section schema already defined: `about_summary`, `responsibilities[]`, `required_qualifications[]`, `preferred_qualifications[]`, `benefits[]`, plus an `extraction_method` tag per job.

**Precondition:** all three tiers require `raw_html` to still exist at ingest time. Today's pipeline flattens to `description_text` before section extraction ever runs — that has to be reordered so Tiers 2–4 run *before* `clean_job_description()` destroys structure, not after. This is the single most important sequencing change; everything below assumes it's done.

---

## Tier 2: HTML DOM Parsing

### Goal

Walk the raw HTML tree while it still has semantic structure (`<h2>`, `<h3>`, `<ul>`, `<strong>`) and split it into `(heading_text, block_content)` pairs. This tier does **not** decide which pair maps to which canonical section — that's Tier 3's job. Tier 2's only responsibility is: turn messy HTML into a clean, ordered list of labeled blocks.

### Why not just use `clean_job_description()`

That function's whole purpose is to flatten for display/search — it's optimized to destroy exactly the signal Tier 2 needs. Don't extend it; build a separate, earlier-running module (`deterministic.py` is the natural home given it's already referenced in the pipeline).

### Libraries

- **`selectolax`** (Lexbor bindings) or **`lxml.html`** — either is fine; `selectolax` is meaningfully faster at scale (matters when re-parsing ~7,200+ jobs and eventually a backfill of the full inventory). Avoid `BeautifulSoup` for the hot path — it's fine for prototyping, too slow for millions of jobs.
- **`readability-lxml`** (or Mozilla's Readability.js via a Node subprocess) is *not* the right tool here — it's built for "extract the one main article," not "preserve multiple sibling sections." Don't reach for it.
- **`html2text`** or a hand-rolled block-splitter for the final text normalization once blocks are identified.

### Algorithm

```
1. Parse raw_html into a DOM tree.
2. Walk top-to-bottom through block-level elements in document order.
3. Maintain a "current heading" pointer, starting as None (pre-heading content
   goes into an implicit "intro" bucket — this becomes Tier 3's "about" candidate).
4. For each node:
   a. If it's a heading tag (h1–h4) → close the previous block, open a new one
      with this node's text as the heading label.
   b. If it's a <p> whose ONLY child is a <strong>/<b> AND that text is short
      (< ~8 words) AND ends without terminal punctuation → treat as a
      pseudo-heading (this is the "strong-as-heading" pattern called out in
      the original doc). Close previous block, open new one.
   c. Otherwise → append this node's text/list-items to the current block.
5. For <ul>/<ol> under a block, preserve each <li> as a separate bullet
   (don't join into one paragraph — Tier 3 and the UI both want bullets).
6. Output: ordered list of {heading_label: str | None, bullets: list[str],
   paragraphs: list[str]}.
```

### Code sketch

```python
# job_ingestion/app/ingestion/extractor/html_blocks.py
from selectolax.parser import HTMLParser
import re

HEADING_TAGS = {"h1", "h2", "h3", "h4"}
PSEUDO_HEADING_MAX_WORDS = 8

def _is_pseudo_heading(p_node) -> str | None:
    """A <p> whose sole content is bold text and reads like a label."""
    strong = p_node.css_first("strong, b")
    if not strong:
        return None
    text = p_node.text(strip=True)
    strong_text = strong.text(strip=True)
    if text != strong_text:
        return None  # there's other text in the <p>, not a pure label
    if len(text.split()) > PSEUDO_HEADING_MAX_WORDS:
        return None
    if text.endswith((".", ":", ";")) and not text.endswith(":"):
        return None  # trailing period suggests a sentence, not a label
    return text

def extract_blocks(raw_html: str) -> list[dict]:
    tree = HTMLParser(raw_html)
    blocks = []
    current = {"heading": None, "bullets": [], "paragraphs": []}

    def flush():
        if current["bullets"] or current["paragraphs"]:
            blocks.append(dict(current))

    for node in tree.body.traverse(include_text=False):
        tag = node.tag
        if tag in HEADING_TAGS:
            flush()
            current = {"heading": node.text(strip=True), "bullets": [], "paragraphs": []}
        elif tag == "p":
            label = _is_pseudo_heading(node)
            if label:
                flush()
                current = {"heading": label, "bullets": [], "paragraphs": []}
            else:
                txt = node.text(strip=True)
                if txt:
                    current["paragraphs"].append(txt)
        elif tag in ("ul", "ol"):
            for li in node.css("li"):
                txt = li.text(strip=True)
                if txt:
                    current["bullets"].append(txt)
    flush()
    return blocks
```

This is deliberately simple — resist the urge to make it smarter. Ambiguity resolution belongs in Tier 3, not here. Tier 2's contract is "structure preserved, not yet classified."

### Platform-specific notes

| ATS | HTML pattern | Tier 2 behavior |
|---|---|---|
| Greenhouse (default theme) | `<p><strong>Responsibilities</strong></p>` then `<ul>` | Hits the pseudo-heading path cleanly |
| Lever | Similar `<strong>`-as-heading, sometimes `<h3>` in custom postings | Mixed — both paths needed |
| Ashby | Often real `<h2>/<h3>` in their default renderer | Clean heading path |
| Custom career pages (Workday, in-house CMS) | Everything from clean semantic HTML to a single `<div>` blob with inline styles | Falls through to fewer/larger blocks; Tier 3 lexicon still runs, just on bigger chunks; heuristic Tier 5 catches total failures |

Don't build a parser-per-platform inside Tier 2 itself. If a specific ATS consistently produces one recognizable pattern, that belongs in Tier 1 (platform-native mapping) as a small dedicated adapter — Tier 2 should stay generic.

### Edge cases to handle explicitly

- **Tables inside JDs** (rare but happens for comp bands or shift schedules) — extract `<td>` text as paragraphs, don't attempt to reconstruct table structure. Not worth the complexity for the volume it affects.
- **Nested `<ul>` inside `<li>`** — flatten one level; deeply nested bullet structure in JDs is a formatting bug on the employer's side, not a structure to preserve faithfully.
- **EEO/legal boilerplate at the end** — Tier 2 doesn't need to strip this; tag it in Tier 3 via a dedicated boilerplate pattern list so it doesn't get misfiled into "benefits" or "qualifications."

---

## Tier 3: Header Lexicon on Preserved Text

### Goal

Given Tier 2's ordered list of `{heading, bullets, paragraphs}` blocks, classify each block's heading into one of the canonical sections: `about`, `responsibilities`, `required_qualifications`, `preferred_qualifications`, `benefits`, `boilerplate`, `other`.

### Why fuzzy matching, not just regex

Plain regex against a fixed synonym list gets you the ~65–70% recall the original doc cites — that's the ceiling of exact-match approaches against the long tail of header phrasing ("Your Day-to-Day," "The Impact You'll Have," "What Success Looks Like"). Fuzzy string matching against a larger, weighted synonym table pushes past that ceiling without adding per-job cost, because it still runs in microseconds.

### Library

**`rapidfuzz`** — fast (Cython), MIT-licensed, drop-in for this use case. Avoid `fuzzywuzzy` (same algorithm, much slower, GPL-adjacent licensing history).

### Synonym table design

Structure as a scored table, not a flat list — some phrases are near-certain, others are weak signals that should only win if nothing else matches:

```python
# job_ingestion/app/ingestion/extractor/section_lexicon.py

SECTION_SYNONYMS: dict[str, list[str]] = {
    "about": [
        "about the role", "about this role", "the role", "role overview",
        "position summary", "the opportunity", "about the team",
        "what you'll join", "overview",
    ],
    "responsibilities": [
        "responsibilities", "key responsibilities", "what you'll do",
        "what you will do", "your day-to-day", "the impact you'll have",
        "day to day", "duties", "core responsibilities", "in this role you will",
        "what you'll be doing", "job duties",
    ],
    "required_qualifications": [
        "requirements", "required qualifications", "minimum qualifications",
        "basic qualifications", "what you'll bring", "what we're looking for",
        "must haves", "you have", "qualifications", "who you are",
        "what you need", "skills required",
    ],
    "preferred_qualifications": [
        "preferred qualifications", "nice to have", "nice-to-haves",
        "bonus points", "preferred skills", "extra credit",
        "it would be great if", "ideally you have",
    ],
    "benefits": [
        "benefits", "perks", "what we offer", "compensation and benefits",
        "why join us", "total rewards", "perks and benefits",
    ],
    "boilerplate": [
        "equal opportunity", "eeo statement", "diversity statement",
        "accommodation", "e-verify", "background check",
    ],
}
```

### Matching logic

```python
from rapidfuzz import fuzz, process

FLAT_LOOKUP = [
    (synonym, section)
    for section, synonyms in SECTION_SYNONYMS.items()
    for synonym in synonyms
]

MATCH_THRESHOLD = 78  # rapidfuzz partial_ratio score, tune against labeled sample

def classify_heading(heading: str | None) -> tuple[str, float]:
    if not heading:
        return "other", 0.0
    heading_norm = heading.lower().strip(" :.-")
    match, score, _ = process.extractOne(
        heading_norm,
        [s for s, _ in FLAT_LOOKUP],
        scorer=fuzz.partial_ratio,
    )
    if score < MATCH_THRESHOLD:
        return "other", score
    section = dict(FLAT_LOOKUP)[match]
    return section, score
```

### Boundary handling (the hard part)

This is where most of the real engineering effort in Tier 3 goes — not the fuzzy matching itself.

1. **"Preferred" embedded mid-list without its own subheading.** Within a `required_qualifications` block, split bullets on lines that themselves start with "preferred," "nice to have," "bonus," etc. Move everything from that line onward to `preferred_qualifications`. This is a per-bullet regex pass, run *after* block-level classification.

2. **First unlabeled block = "about."** If the first block in Tier 2's output has `heading = None` and consists of paragraphs (not bullets), map it to `about` even without a lexicon hit. If it consists of bullets instead, don't force it — an opening bullet list is usually the start of responsibilities, not a summary; let it fall through as `other` and get picked up by Tier 5's heuristic ("first paragraph → about") only if no `about` block exists anywhere.

3. **Company "About Us" mixed into the role description.** Distinguish via a secondary keyword check on paragraph content, not just the heading: if a block classified as `about` contains strong company-marketing signals ("founded in," "our mission," "headquartered in") and is *not* the first block, downgrade it to `other`/drop it — it's boilerplate about the company, not the role.

4. **Boilerplate at the bottom.** Anything classified `boilerplate` gets excluded from all canonical sections entirely — don't merge it into benefits even if the heading fuzzy-matches something benefits-adjacent (e.g., "Our Commitment to You" can go either way; check for EEO-specific phrases first as a higher-priority override before the general lexicon runs).

5. **Multiple blocks mapping to the same section.** Don't dedupe by discarding — concatenate bullets in document order. It's common for "Requirements" to appear once near the top as a summary and again lower down with more detail; both are legitimately `required_qualifications`.

### Expected recall and where the remaining gap goes

Budget for **~80–85% coverage** from Tiers 1–3 combined on well-formed ATS HTML, based on the ceiling regex-only approaches hit (~65–70%) plus the lift fuzzy matching + the boundary rules above typically provide. The remaining long tail — genuinely novel phrasing, single-paragraph JDs with no headers at all, heavily customized career pages — is Tier 4's job, not a reason to keep expanding the synonym table indefinitely. Track `section_extraction_method` per job so you can see this split empirically rather than guessing.

---

## Tier 4: Small Classifier for the Long Tail

### Goal

Handle the cases where Tier 3 returns `other` or leaves a block unclassified — genuinely novel header phrasing, or paragraph blocks with no heading at all that need to be sorted by content rather than by label.

### Why a small classifier and not more lexicon entries

Synonym tables have a ceiling: every new employer's idiosyncratic phrasing ("The Adventure Ahead," "Your Mission Should You Choose to Accept It") needs a human to notice, add, and validate it. A small classifier generalizes to unseen phrasing without manual upkeep, at inference cost that's negligible compared to the generative LLM path it's replacing.

### Model choice

- **DistilBERT or a similarly small encoder** (not a generative LLM, not full BERT-large) fine-tuned as a **multi-class text classifier** over the same six labels used in Tier 3 (`about`, `responsibilities`, `required_qualifications`, `preferred_qualifications`, `benefits`, `other/boilerplate`).
- Input unit is a **block** (heading text + first ~2 bullets/sentences concatenated), not the whole JD — classify at the same granularity Tier 3 operates on so the two tiers slot together.
- Self-hosted inference (ONNX-exported, CPU is fine at this size and volume) — no per-job external API cost, no queue dependency. This directly addresses the cost/latency/non-determinism complaints the original doc raises about the LLM approach, while still generalizing better than pure lexicon matching.

### Bootstrapping labels without manual annotation

You already have the training signal sitting in your existing enrichment output — this is the cheapest possible way to get a labeled dataset:

1. Take a sample of a few thousand jobs (aim for coverage across your top ATS platforms and a good chunk of "custom career page" jobs, since that's the long tail you're targeting).
2. Run Tier 2 to get blocks, run Tier 3 to classify what it can.
3. For blocks Tier 3 leaves as `other`/unclassified, use the **existing Gemini enrichment output** (which already produced `responsibilities`/`qualifications`/`benefits` arrays for these jobs) as a noisy label source: fuzzy-match each unclassified block's text against the enrichment arrays to infer which array it most likely came from.
4. Treat this as **noisy pseudo-labeling**, not ground truth — spot-check a few hundred by hand before training, and drop low-confidence matches rather than forcing a label.
5. Fine-tune on this bootstrapped set. Held-out validation should still be a small hand-labeled set (a few hundred blocks) so your accuracy number isn't circular.

This is the key move: you're not paying for a new labeling effort, you're **converting the LLM cost you're already paying today into a one-time training cost**, then turning the recurring LLM spend off for this specific task.

### Where it slots into the pipeline

```
Tier 2 (blocks) → Tier 3 (lexicon+fuzzy) → unresolved blocks → Tier 4 (classifier)
                                                              → still unresolved → Tier 5 (heuristic)
```

Tier 4 should only ever see what Tiers 1–3 couldn't resolve — don't run it on every block by default, both for cost and because Tier 3's decisions on clear matches are more auditable/debuggable than a model's.

### What "success" looks like here

- Model runs synchronously in the ingest pipeline (no queue), CPU inference, sub-100ms per job — keeps the "pipeline-synchronous" property the doc's comparison table calls out as an advantage over the LLM path.
- No hallucination risk by construction — it's a classifier over existing text spans, not a generator; it can misfile a block, but it can't invent or rewrite content, which directly resolves the "rewrite risk" and compliance-sensitive-field concern from the original doc.
- Deterministic given a fixed model version — same input always gives same output, unlike a generative model across prompt/model-version changes. Pin and version the model artifact the same way you'd version a database migration.

---

## Orchestration across Tiers 2–4

```python
def extract_sections(raw_html: str, platform: str) -> JobSections:
    # Tier 1 short-circuits before this function is even called,
    # if platform-native fields exist.

    blocks = extract_blocks(raw_html)              # Tier 2
    sections = JobSections()

    for block in blocks:
        label, score = classify_heading(block["heading"])   # Tier 3
        if label == "other" and score < MATCH_THRESHOLD:
            label = classify_block_content(block)            # Tier 4
        sections.append(label, block)

    sections.apply_preferred_split()   # boundary rule #1 above
    sections.apply_boilerplate_filter()
    if not sections.about:
        sections.about = heuristic_about_fallback(blocks)     # Tier 5

    sections.extraction_method = infer_dominant_method(sections)
    return sections
```

Log `extraction_method` per job as originally proposed (`platform_native`, `html_dom`, `header_lexicon`, `classifier`, `heuristic`) — this is what lets you monitor which tier is actually doing the work over time, catch a platform's empty-section rate spiking, and decide whether Tier 4's training data needs refreshing.

## Rollout sequencing

1. Ship Tier 2 + Tier 3 first — they require no training data and already close most of the gap.
2. Add the publish gate (minimum section coverage, not just `processing_state = success`) once Tiers 2–3 are live, so you can measure real coverage before adding Tier 4.
3. Backfill existing `success` jobs with empty sections from `raw_jobs.raw_html` using Tiers 2–3 only, as a first pass — cheap and immediate.
4. Bootstrap and ship Tier 4 once you have real Tier 3 `other`-rate data telling you the long tail is big enough to be worth it. Don't build the classifier speculatively before Tiers 2–3 are measured in production.
5. Only after all of this, revisit whether the LLM enrichment prompt should drop section extraction entirely — that's a config change once you trust the new pipeline's coverage numbers.
