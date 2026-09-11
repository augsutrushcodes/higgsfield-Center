---
name: hfc-higgsfield
description: >
  Use when the user asks about Higgsfield AI — writing or refining video/image
  prompts, choosing among Kling / Sora / Veo / Wan / Seedance / Hailuo / DoP /
  Soul / Nano Banana / Seedream / Flux / GPT Image, camera controls, named
  motion presets, Soul ID character consistency, Cinema Studio, Marketing
  Studio, Canvas, Seedance 2.0 or 2.5, or any mention of higgsfield.ai. Also
  use when the Higgsfield MCP connector or CLI is being driven.
metadata:
  tags: [higgsfield, video, image, prompt, cinematic, seedance, kling, soul, mcp]
  version: 0.1.0
  updated: 2026-09-11
  parent: higgsfield-center
  status: draft
---

# Higgsfield

Higgsfield hosts many generation engines on one platform — video (Kling, Sora 2,
Veo, Wan, Seedance, Minimax Hailuo, FLUX 3 Video, Higgsfield DoP), images (Soul,
Kling Image, Nano Banana, Seedream, GPT Image, Flux), a large named
motion-preset library, the Soul ID character-consistency system, Cinema Studio,
Marketing Studio, Canvas, and one-click Apps.

## QUICK FACTS

*Routing aids. Read the sections for the actual rules.*

- **Do not re-implement the prompt library.** OSideMedia's MIT-licensed skill
  already covers this in depth — install it and route to it
  [→](#dont-duplicate-the-existing-library)
- Prompt contract is **MCSLA**: Model · Camera · Subject · Look · Action
  [→](#mcsla)
- **Aspect ratio is an enum, not a free-form value** — check the model's
  allowed ratios before writing a header [→](#verify-before-you-commit)
- `2.35:1` / "anamorphic" is **style vocabulary for the Look line**, never an
  output ratio [→](#verify-before-you-commit)
- Name **exact preset names**. The platform matches them literally; a plausible
  invented name silently does nothing [→](#verify-before-you-commit)
- Image-to-video: describe **only what moves or changes**, never what is already
  in the frame [→](#mcsla)
- Prompt construction and prompt *execution* are separate layers — keep them
  separate [→](#execution-surfaces)
- This session has the **Higgsfield MCP connector** loaded
  [→](#execution-surfaces)

## Don't duplicate the existing library

[OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)
is a mature, MIT-licensed Higgsfield prompt library — 33 sub-skills, a
verification spine over the model catalogue, genre templates, a generation
ledger. Re-typing a worse version of it into this repo would be strictly
negative value.

**So this file is a router, not a replacement.** Install theirs alongside:

```bash
git clone https://github.com/OSideMedia/higgsfield-ai-prompt-skill \
  ~/.claude/skills/higgsfield
```

> **Name collision:** their root skill is named `higgsfield`. Everything in this
> repo is prefixed `hfc-` specifically so both can be installed at once without
> the router ambiguity. Keep that prefix.

What belongs **in this file** rather than theirs:

- how Higgsfield sits next to Luma and Beeble in a cross-platform decision
- your own house defaults, house style, recurring characters, project conventions
- anything you learn that theirs doesn't cover

A full structural record of their library — architecture, conventions, tooling,
the patterns worth reusing — is in
[`knowledge/higgsfield-ai-prompt-skill-teardown.md`](../../knowledge/higgsfield-ai-prompt-skill-teardown.md).

## MCSLA

Five layers, every video prompt:

| Letter | Layer | Example |
|---|---|---|
| **M** | Model | Kling 3.0 |
| **C** | Camera | FPV drone weaving through the alley |
| **S** | Subject | A woman in a tactical jacket |
| **L** | Look | Cold blue shadows, hard practical key, 16:9 |
| **A** | Action | She sprints, slides under a gate |

Supporting rules:

- `Subject → Action → Camera → Style` is the most reliable ordering.
- Keep short-form prompts under ~200 words. Going over is usually padding
  rather than locking. (Long block-scaffold production prompts are a different
  regime with their own structure — the word cap doesn't govern those.)
- One primary action per clip; one or two secondary at most.
- Don't leave a generic emotion in a prompt. "Sad" doesn't render — decompose
  into what a camera sees: breath, eyes, jaw, shoulders, what the hands do.
- Recurring character: split the prompt into an **identity block** and a
  **motion block** and never mix them. Identity is what stays constant across
  shots; motion is what this shot does.

## Verify before you commit

The failure this prevents: a model's training knows the *rough shape* of
Higgsfield — enough to produce a preset name or a flag that looks right and
isn't. The platform matches names literally, so a plausible invention silently
does nothing while costing credits.

Check these against the live catalogue or a dated spec, never from memory:

- **Aspect ratio** — an enum, per model. Seedance 2.0 supports native 21:9;
  Kling 3.0 does not. `2.35:1` / `2.39:1` / "anamorphic" are **Look-line style
  register**, not output ratios. Mixing those up is the canonical mistake here.
- **Duration** — a model-dependent enum, not a free number.
- **Camera and motion preset names** — exact strings.
- **Model names and versions** — the lineup changes between releases.
- **CLI flag forms and MCP parameter names** — verify, don't pattern-match.

With the MCP connector loaded, `models_explore` returns the live schema. That
call is cheap and it is sitting right there — make it rather than guessing.

## Execution surfaces

Prompt construction and prompt execution are separate layers. This repo does
the first. Higgsfield ships three surfaces for the second:

| Surface | For | Entry point |
|---|---|---|
| **MCP connector** | claude.ai web / desktop / this session | `https://mcp.higgsfield.ai/mcp` |
| **CLI** | terminal-native agents (Claude Code, Cursor) | `github.com/higgsfield-ai/cli` |
| **Bundled skills** | Cowork-style skill consumers | `npx skills add higgsfield-ai/skills` |

A Higgsfield account is required for all three. Higgsfield's own guidance is to
prefer the CLI when working in a terminal.

**This session has the MCP connector loaded** — tools are available for
generation (`generate_image`, `generate_video`, `generate_audio` and their
batch forms), model discovery (`models_explore`), cost and balance checks
(`balance`, `show_plans_and_credits`), media upload (`media_upload_widget`),
and the studio surfaces (Marketing Studio, Shorts Studio, Canvas, Scene
Builder 3D, Personal Clipper).

### Preflight

Before an expensive video generation:

1. **Schema check** — `models_explore` for the model's real parameter enums.
2. **Cost estimate** — `generate_video(..., get_cost: true)` returns credits
   without submitting a job.

Surface this when execution intent is signalled *and* a video-class or
high-cost model is named, or when budget comes up. Not on every request.

## Cross-platform routing

| Job | Platform |
|---|---|
| Multi-shot production with character consistency across scenes | **Higgsfield** (Soul ID, Cinema Studio) |
| Named motion / VFX preset library | **Higgsfield** |
| Platform-native ad formats with preset hooks | **Higgsfield** Marketing Studio |
| Output must grade alongside real camera footage (HDR/ACES EXR) | **Luma** Ray3.2 |
| Precise beat timing across a clip (up to 16 keyframes) | **Luma** multi-keyframe |
| Relight, composite, pull passes on footage that already exists | **Beeble** |
| SDR footage that needs to reach 16-bit before a grade | **Beeble** SDR→HDR |

## TODO before this leaves `status: draft`

- [ ] Record house defaults: preferred models, ratios, durations, look
- [ ] Note recurring Soul IDs / characters and where their references live
- [ ] Capture project conventions worth reusing (naming, folder layout)
- [ ] Add anything learned that the OSideMedia library doesn't cover
