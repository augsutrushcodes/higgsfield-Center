# Higgsfield Center

A cross-platform Claude skill library for AI creative generation. One router
that decides **which platform**, then **which model**, then **what the prompt
actually says**.

Covers [Higgsfield](https://higgsfield.ai), [Luma](https://lumalabs.ai) and
[Beeble](https://beeble.ai) today, with more added as they're researched.

> **Status: early.** All three platform files are `status: draft` — verified
> where marked with a date, with explicit `UNVERIFIED` blocks and a TODO list
> where not. That's deliberate: a marked gap is useful, a confident guess is not.

## Why a router and not one big skill

These platforms are mostly **not** alternatives to each other. They sit in
different lanes:

| Lane | Meaning | Platform |
|---|---|---|
| **Generate** | make footage or stills that didn't exist | Higgsfield, Luma |
| **Direct** | control what happens *when* inside a clip | Luma (16 keyframes), Higgsfield (Cinema Studio) |
| **Transform** | change footage that already exists | Luma (Modify Video), Higgsfield (Seedance VFX), Beeble (SwitchX) |
| **Finish** | relight, composite, passes, colour depth | Beeble |

Real jobs cross lanes. Generate in one place, finish in another. The router
exists to make that chain obvious instead of forcing a false either/or.

## Layout

```
SKILL.md                       root dispatcher — routing table, tie-breaks, load map
skills/
  higgsfield/SKILL.md          Higgsfield — routes to the OSideMedia library, adds house rules
  luma/SKILL.md                Luma — Ray3.2 video, UNI-1.1 image, keyframes, HDR/EXR
  beeble/SKILL.md              Beeble — relight, composite, passes, SDR→HDR
  shared/prompt-craft.md       cross-platform craft: markers, mechanism, iteration, anti-bombast
  _template/SKILL.md           scaffold for the next platform
knowledge/
  higgsfield-ai-prompt-skill-teardown.md   full structural record of the OSideMedia library
  skill-authoring-playbook.md              how to grow this repo without it rotting
  research-queue.md                        intake for platforms not yet covered
scripts/validate.py            frontmatter, routing parity, links, staleness, unverified count
workspace/                     git-ignored working area: input/ → processed/, output/
```

## Install

**Claude Code**

```bash
git clone https://github.com/augsutrushcodes/higgsfield-Center ~/.claude/skills/higgsfield-center
```

**Claude Cowork** — drop the folder into your workspace. `SKILL.md` at the root
is the dispatcher.

**Claude.ai Projects** — `SKILL.md` as the instruction base, files from
`skills/` as project documents.

### Install alongside the OSideMedia Higgsfield library

Recommended. That library is far deeper on Higgsfield specifically than this
repo will ever be, so `skills/higgsfield/SKILL.md` routes to it rather than
duplicating it:

```bash
git clone https://github.com/OSideMedia/higgsfield-ai-prompt-skill ~/.claude/skills/higgsfield
```

Every skill name here is prefixed `hfc-` so both install cleanly side by side.
Their root skill is named `higgsfield`; the prefix is what keeps the router
unambiguous. Keep it.

## The rule this repo is built around

**Never write a platform fact from memory.**

A model's training knows the rough shape of every AI creative tool — that there
are aspect ratios, that there are durations, that flags look roughly like
`--aspect-ratio`. That's exactly enough to produce something plausible and
wrong. A wrong preset name silently does nothing. A wrong enum costs credits.

So every factual claim here carries provenance:

```markdown
> **Verified 2026-09-11** — https://lumalabs.ai/llm-info
```

and anything unchecked is marked `UNVERIFIED` with a note on what would confirm
it. Verification older than 30 days is treated as stale.

## Validate

```bash
python3 scripts/validate.py            # health check
python3 scripts/validate.py --strict   # warnings become failures
```

Pure stdlib, no dependencies. Checks the frontmatter contract, that every
platform on disk is routed from the dispatcher, that relative links resolve,
flags stale verification dates, and counts unverified blocks. Runs in CI on
every push and PR.

## Adding a platform

1. Copy `skills/_template/SKILL.md` into `skills/<platform>/SKILL.md`
2. Fill it from a **primary source** — vendor docs, changelog, pricing page.
   Not a review site, not a video summary, not memory.
3. Add a routing row to the root `SKILL.md`, plus a tie-break row if it
   collides with something already there
4. `python3 scripts/validate.py`

The intake checklist is in [`knowledge/research-queue.md`](knowledge/research-queue.md);
conventions and growth order are in
[`knowledge/skill-authoring-playbook.md`](knowledge/skill-authoring-playbook.md).

## Credits

Architecture modelled on
[OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
(MIT). No text copied. See [`CREDITS.md`](CREDITS.md).

MIT licensed. Unofficial and independent — platform names and trademarks belong
to their owners.
