# Changelog

## v0.1.0 — 2026-09-11

Initial scaffold. A cross-platform router plus the research behind it.

### Added

- **Root `SKILL.md`** — dispatcher with an 8-item pre-delivery checklist, a
  lane-first routing model (generate / direct / transform / finish), a routing
  table, five tie-break rows for genuinely colliding platforms, and a load map
  that caps how much gets read per request.
- **`skills/higgsfield/SKILL.md`** — deliberately a *router*, not a
  re-implementation. OSideMedia's MIT library already covers Higgsfield
  prompting in depth; this file points at it, holds the MCSLA summary and the
  verify-before-you-commit rules, documents the three execution surfaces
  (MCP / CLI / bundled skills), and reserves space for house defaults.
- **`skills/luma/SKILL.md`** — Ray3.2 video and UNI-1.1 image, multi-keyframe
  direction (16 per clip), Modify Video V2, Reframe, Draft Mode, native 16-bit
  HDR with ACES2065-1 EXR export, API tiers. Verified against Luma's own
  LLM-facing page. Two `UNVERIFIED` blocks left standing on duration and
  aspect-ratio enums rather than guessed.
- **`skills/beeble/SKILL.md`** — the finishing lane: Canvas node graph,
  SwitchX, background remover, VFX Pass Generator, 3D Relight, SDR→HDR, cloud
  vs Studio, Nuke / Blender / Unreal plugins. Includes the colour-depth
  handoff rule — Luma output is already 16-bit, so running SDR→HDR on it is
  wasted work.
- **`skills/shared/prompt-craft.md`** — cross-platform craft: visible markers
  over proper names, emotion decomposed into mechanism, anti-bombast, one
  action per clip, describe-only-what-changes for i2v and v2v, lock before
  generating, falsifiable criteria first, and the systematic-vs-stochastic
  fork that decides whether iterating is even the right move.
- **`skills/_template/SKILL.md`** — scaffold for the next platform, with the
  provenance markers and TODO list built in.
- **`knowledge/higgsfield-ai-prompt-skill-teardown.md`** — standalone
  structural record of OSideMedia's v3.35.0 library: dispatcher pattern, the
  33 sub-skills, the frontmatter contract, the verification spine over the
  model catalogue, the append-only generation ledger, the 9 discipline
  patterns, the tooling and release gate, and a what-to-steal / what-not-to
  list. Written to survive without the clone.
- **`knowledge/skill-authoring-playbook.md`** — the conventions, reordered as
  what to do next, including the growth order that avoids writing thirty stale
  files in a weekend.
- **`knowledge/research-queue.md`** — intake for Runway, Kling direct, Pika,
  Midjourney, ElevenLabs, Suno/Udio, Topaz and aggregators, with the
  verification checklist and three open questions recorded.
- **`scripts/validate.py`** — pure-stdlib gate: frontmatter contract,
  dispatcher↔disk routing parity, relative-link resolution, 30-day
  verification staleness, and an `UNVERIFIED` count. `--strict` promotes
  warnings to failures.
- **CI** (`.github/workflows/validate.yml`) — runs the validator on every push
  and PR, then a two-directional self-check asserting it still fails on an
  unrouted platform and on a missing `hfc-` name prefix.
- **`CREDITS.md`**, MIT `LICENSE`, `CONTRIBUTING.md`, `CLAUDE.md`,
  `workspace/` (input → processed, output), `.claude/commands/validate.md`.

### Conventions established

- Every factual claim carries `**Verified YYYY-MM-DD**` with a primary source,
  or is marked `**UNVERIFIED**` with what would confirm it. Over 30 days is
  stale.
- Sub-skill names use the `hfc-` prefix so this library and OSideMedia's
  upstream `higgsfield` skill can be installed together without router
  ambiguity.
- The pre-delivery checklist has exactly one canonical home (root `SKILL.md`);
  everywhere else cites it by number.
