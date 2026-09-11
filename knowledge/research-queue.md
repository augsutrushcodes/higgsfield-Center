# Research Queue

Intake for "when I find more info and skills." Drop links, notes and
screenshots here as you find them; they get promoted into a platform skill once
there's a primary source behind them.

**Statuses:** `idea` → `researching` → `drafted` → `live` (has a routed
`skills/<platform>/SKILL.md`)

---

## Live

| Platform | Skill | Verified on | Notes |
|---|---|---|---|
| Higgsfield | [`skills/higgsfield/`](../skills/higgsfield/SKILL.md) | 2026-09-11 | Thin router into the OSideMedia library; not a re-implementation |
| Luma | [`skills/luma/`](../skills/luma/SKILL.md) | 2026-09-11 | Ray3.2 + UNI-1.1 from Luma's own LLM-facing page |
| Beeble | [`skills/beeble/`](../skills/beeble/SKILL.md) | 2026-09-11 | VFX/relight lane — the "fix it in post" side, not text-to-video |

## Candidates

Not researched yet. Add rows freely — an empty row is a better record than a
browser tab.

| Platform | Lane | Status | Source to check | Why it might earn a slot |
|---|---|---|---|---|
| Runway | text-to-video, video edit | idea | runwayml.com | Gen-family models, strong edit tooling |
| Kling (direct) | text/image-to-video | idea | klingai.com | Already reachable via Higgsfield; direct surface may differ |
| Pika | short-form video, effects | idea | pika.art | Effects-led, social-native |
| Midjourney | stills, video | idea | midjourney.com | Style reference system is its own dialect |
| ElevenLabs | voice, SFX, dubbing | idea | elevenlabs.io | Audio lane is currently unrepresented |
| Suno / Udio | music | idea | — | Music is a separate lane from SFX/VO |
| Topaz | upscale, frame interp | idea | topazlabs.com | Finishing lane |
| Freepik / Krea | aggregators | idea | — | Multi-model front-ends; routing may overlap Higgsfield |

## Intake checklist

Before a candidate moves to `drafted`, get these from a **primary source**
(the vendor's own docs, changelog, or pricing page — not a review site, not a
YouTube summary, not model memory):

- [ ] What lane is it actually in? (generate / edit / relight / finish / audio)
- [ ] Current model names and version numbers, with the date you checked
- [ ] Hard limits: max duration, resolutions, aspect-ratio **enums**
- [ ] Reference/conditioning inputs it accepts, and how many
- [ ] Whether it has an API, CLI, or MCP surface
- [ ] Official prompting guidance, if any — vendors often publish a dialect
- [ ] Pricing/credit model, well enough to say when it's the expensive choice
- [ ] The one thing it does that nothing else on the list does

That last line is the real test. If it can't be answered, the platform doesn't
need a skill file — it needs a row in the routing table pointing somewhere else.

## Open questions

- **Luma version drift.** Luma's LLM-facing page named **Ray3.2** and
  **UNI-1.1** on 2026-09-11; third-party reviews from earlier in 2026 refer to
  **Ray3.14**. Treated the official page as authoritative. Re-check before
  quoting any version number.
- **Beeble API.** `docs.beeble.ai` advertises an index at
  `docs.beeble.ai/llms.txt` — not yet read. Worth pulling for exact node and
  pass names.
- **Overlap policy.** Kling is reachable both through Higgsfield and directly.
  Decide whether platform skills route by *vendor* or by *surface* before
  adding a second overlapping entry, or the routing table will contradict
  itself.
