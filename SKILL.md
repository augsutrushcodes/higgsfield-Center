---
name: higgsfield-center
description: >
  Use for any AI creative-generation work across platforms — writing or refining
  video / image / audio prompts, choosing which platform or model fits a shot,
  planning a multi-stage production, or troubleshooting a bad generation. Covers
  Higgsfield, Luma (Dream Machine / Ray3 / UNI), and Beeble (AI VFX, relight,
  compositing), with more platforms added over time. Also trigger on generic
  "write me a video prompt" or "which AI tool should I use for X" requests.
user-invocable: true
metadata:
  tags: [ai-video, ai-image, prompt, cinematic, higgsfield, luma, beeble, vfx]
  version: 0.1.0
  updated: 2026-09-11
  license: MIT
---

# Higgsfield Center

A cross-platform router for AI creative-generation work. One place to decide
**which platform**, then **which model**, then **what the prompt actually says**.

---

## Pre-delivery checklist

Run these before sending a response. Not prohibitions — a checklist that fires
at the moment it's needed.

1. **Routing line first.** Open with one line naming what you routed to
   (e.g. "Routing to `hfc-luma` — multi-keyframe is the right control here").
   One line, then the work.

2. **Routed files actually opened.** Match the request to the routing table and
   **read** the file. A grep snippet does not satisfy this. Platform facts move
   between releases; that is the entire reason the file exists.

3. **No platform fact from memory.** Model names, version numbers, duration and
   aspect-ratio enums, preset names, flag forms, parameter names — these come
   from a platform file with a verification date, or from a live check. The
   failure this prevents is **plausible-and-wrong**: training data knows the
   rough shape of every one of these tools, which is exactly enough to invent
   something that looks right and silently does nothing.

4. **Check the verification date.** A platform file marked `verified` more than
   **30 days** ago is stale. Say so, or re-verify, before quoting a number from
   it. A fact with no date is not a verified fact.

5. **Aspect ratio and duration are enums.** Per model. `2.35:1` / `2.39:1` /
   "anamorphic" is **style vocabulary**, never an output ratio.

6. **Shared craft applied.** Visible markers not proper names; emotion
   decomposed into mechanism; named mechanisms not adjective stacks; one primary
   action per clip. → [`skills/shared/prompt-craft.md`](skills/shared/prompt-craft.md)

7. **Cost surfaced when it matters.** If execution is actually going to happen
   *and* the model is video-class or high-cost, or budget was raised — check
   schema and estimate cost before submitting. Not on every request.

8. **Unverified marked, not hidden.** If a needed fact isn't confirmed, say
   `UNVERIFIED` and say what would confirm it. An honest gap beats a confident
   guess.

If any item is unmet, the response isn't finished.

---

## Route by lane first

The most common routing mistake is treating every platform as an alternative to
every other. They're mostly in different lanes:

| Lane | Meaning | Platform |
|---|---|---|
| **Generate** | make footage/stills that didn't exist | Higgsfield, Luma |
| **Direct** | control what happens *when* inside a clip | Luma (keyframes), Higgsfield (Cinema Studio) |
| **Transform** | change footage that already exists | Luma (Modify Video), Higgsfield (Seedance VFX), Beeble (SwitchX) |
| **Finish** | relight, composite, passes, colour depth | Beeble |

A full job usually crosses lanes. Chain them; don't pick one.

## Routing table

| User wants | Route to |
|---|---|
| Higgsfield anything — prompts, Soul ID, Cinema Studio, Seedance, Kling, Marketing Studio, Canvas, Apps | [`skills/higgsfield/`](skills/higgsfield/SKILL.md) |
| Luma, Dream Machine, Ray3 / Ray3.2, UNI-1.1, Modify Video, keyframes, Reframe, Draft Mode | [`skills/luma/`](skills/luma/SKILL.md) |
| Beeble / "Beebl", SwitchX, relight, compositing, PBR / alpha / depth passes, SDR→HDR, Nuke / Blender / Unreal plugins | [`skills/beeble/`](skills/beeble/SKILL.md) |
| Prompt craft that isn't platform-specific — markers, emotion, iteration, anti-bombast | [`skills/shared/prompt-craft.md`](skills/shared/prompt-craft.md) |
| "Which platform should I use for X" | this file — see the tie-breaks below |
| Adding a new platform to this library | [`skills/_template/SKILL.md`](skills/_template/SKILL.md) + [`knowledge/skill-authoring-playbook.md`](knowledge/skill-authoring-playbook.md) |
| Notes / links / candidates for platforms not yet covered | [`knowledge/research-queue.md`](knowledge/research-queue.md) |
| How the OSideMedia Higgsfield library is built, and what to reuse from it | [`knowledge/higgsfield-ai-prompt-skill-teardown.md`](knowledge/higgsfield-ai-prompt-skill-teardown.md) |

### Tie-breaks

For the pairs that genuinely collide. Each has the disambiguating question.

| Collision | Decide by |
|---|---|
| **Higgsfield vs Luma** for a single shot | Does the output have to **grade next to real camera footage**? → Luma (native 16-bit HDR, ACES EXR). Does it need **character consistency across many shots**? → Higgsfield (Soul ID). Neither → whichever you have credits on. |
| **Higgsfield vs Luma** for timing control | Do specific things have to happen at specific **moments**? → Luma multi-keyframe (up to 16). Is it a **multi-shot sequence** rather than beats inside one clip? → Higgsfield Cinema Studio. |
| **Transform: Luma vs Higgsfield vs Beeble** | Restyle or alter generated-looking footage → Luma Modify Video or Higgsfield Seedance VFX. **Relight, composite, or pull passes on a real plate** → Beeble. Beeble is the only one that emits alpha/depth/PBR. |
| **Beeble vs "just regenerate"** | Is there a **source plate** worth preserving? Yes → Beeble. No → generate instead; Beeble's starting point is footage. |
| **SDR→HDR: needed or not** | What is the source's colour depth? Luma Ray3.2 output is already 16-bit HDR — converting it again is wasted work. Phone footage and most generated video are 8-bit and do need the pass. |

## Load map

The routing table says *where*. This says *how much*.

| Situation | Load |
|---|---|
| Simple prompt, platform already named | this file + that one platform file |
| Cross-platform "which tool" question | this file only — the tie-breaks answer it |
| Prompt craft question, no platform named | `skills/shared/prompt-craft.md` |
| Multi-stage production crossing lanes | this file + each platform file in the chain |
| Adding a platform | `_template` + the playbook |
| Anything else | one routing row → that file. Resist loading more than the row names. |

---

## Working folders

| Folder | Use |
|---|---|
| `workspace/input/` | Things to read: briefs, scripts, references, plates. Look here first when the user says "the file I gave you." |
| `workspace/output/` | Everything produced for the user. Never the repo root. Give the path when done. |
| `workspace/processed/` | Inputs finished with. **Move** them here — never delete a user's file. |

Contents are git-ignored. Don't assume anything in them is committed.

---

## Status

Early. All three platform files are `status: draft` — verified where marked,
with explicit `UNVERIFIED` blocks and a TODO list where not.

`python3 scripts/validate.py` checks the frontmatter contract, that every
platform on disk is routed from this table, that relative links resolve, and
reports stale verification dates and unverified blocks.

Growth plan and conventions:
[`knowledge/skill-authoring-playbook.md`](knowledge/skill-authoring-playbook.md).
