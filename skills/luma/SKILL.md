---
name: hfc-luma
description: >
  Use when the user asks about Luma AI, Dream Machine, the Luma app, Ray3 /
  Ray3.2 video generation, UNI-1.1 image generation, Modify Video, multi-keyframe
  direction, Reframe, Draft Mode, HDR / EXR / ACES output from generated video,
  or the Luma API. Also use when choosing between Luma and another video
  platform for a shot.
metadata:
  tags: [luma, dream-machine, ray3, uni-1, video, image, hdr, keyframe]
  version: 0.1.0
  updated: 2026-09-11
  parent: higgsfield-center
  status: draft
---

# Luma

> **Verified 2026-09-11** — <https://lumalabs.ai/llm-info> (Luma's own
> LLM-facing information page). Model versions move fast; re-check anything
> older than 30 days before quoting a number.

## QUICK FACTS

*Routing aids. Read the sections for the actual rules.*

- Two current models: **Ray3.2** for video, **UNI-1.1** for image [→](#models)
- Ray3.2's distinguishing feature is **native 16-bit HDR with ACES2065-1 EXR
  export** — it is the lane to pick when output must be graded alongside real
  camera footage [→](#when-to-pick-luma)
- **Multi-Keyframe: up to 16 keyframes per clip** — the strongest structural
  control on this list [→](#multi-keyframe)
- **Modify Video V2** transforms existing footage up to **20 s at 1080p** —
  this is a video-to-video lane, not just text-to-video [→](#modify-video)
- **UNI-1.1 takes up to 9 reference inputs** and reasons before generating;
  roughly **31 s per image** [→](#models)
- **Draft Mode** exists for cheap exploration — use it before committing to a
  full-quality roll [→](#workflow)
- Surfaces: Luma app (browser + iOS) and the **Luma API** with Python and
  JS/TS SDKs [→](#surfaces)

## Models

### Ray3.2 — video

| Capability | Detail |
|---|---|
| Modes | text-to-video, image-to-video |
| Modify Video V2 | existing footage, up to 20 s, 1080p |
| Multi-Keyframe | up to 16 keyframes per clip |
| Reframe | re-target a clip to any aspect ratio |
| Colour | native 16-bit HDR; EXR export at ACES2065-1 |
| Draft Mode | fast, low-cost exploration pass |

> **UNVERIFIED** — per-request duration and aspect-ratio **enums** for standard
> generation (as opposed to the 20 s Modify Video ceiling). Get these from the
> API reference before writing them into a prompt header. Do not assume they
> match any other platform's.

### UNI-1.1 — image / multimodal

| Capability | Detail |
|---|---|
| Modes | text-to-image, reference-guided, source-grounded |
| References | up to 9 inputs per request |
| Behaviour | multimodal reasoning — "thinks before it generates" |
| Speed | ~31 s per image |
| Range | culture-aware across aesthetics and styles |

## When to pick Luma

Route **to** Luma when:

- output has to survive a **colour grade** next to real footage — the 16-bit
  HDR / ACES EXR path is the reason this platform is on the list at all
- the shot needs **structural control across its length**: specific things
  happening at specific moments. 16 keyframes is a storyboard, not a vibe.
- you already have footage and want to **transform** it (Modify Video V2)
- the same clip is needed in several aspect ratios (Reframe) rather than
  regenerated per ratio
- an image needs **many references** held at once (up to 9)

Route **away** when:

- the job is a full multi-shot production pipeline with character consistency
  across scenes → that is Higgsfield's lane
- the job is relighting or compositing over real plates with per-pass control
  → that is Beeble's lane
- the deliverable is a platform-native ad format with preset hooks → Higgsfield
  Marketing Studio

## Multi-keyframe

16 keyframes per clip is the highest-leverage feature here and the one most
often left unused. Treat it as a shot plan:

- Write the beats **before** generating — a keyframe you invent mid-iteration
  drifts from the original intent.
- Keyframes constrain *layout and motion*, so they are the fix for "the action
  happens at the wrong moment" — a class of problem that prompt rewording
  handles badly.
- More keyframes is not automatically better. Each one is a constraint the
  model must satisfy; over-constraining produces stiff interpolation.

> **UNVERIFIED** — exact keyframe input format and whether timing is specified
> per keyframe or inferred. Check the API reference.

## Modify video

Video-to-video, up to 20 s at 1080p. The 2026 release notes call out improved
motion consistency specifically for this mode.

Same discipline as any v2v lane: the source clip's camera move and subject are
what you're *preserving*. Say what changes; don't re-describe what's already in
the frame. (Same rule as image-to-video everywhere — describe only what moves
or changes.)

## Workflow

1. **Draft Mode first.** Explore cheaply. Lock composition and beats there.
2. **Write falsifiable criteria** before the full-quality roll — what would
   make this shot a reject? Decide now, not after you've seen it.
3. **Full quality roll** once the draft answers the question.
4. **Reframe** for additional ratios instead of regenerating.
5. **EXR/ACES export** only when the shot is going into a graded timeline —
   it's a much heavier file otherwise.

## Surfaces

| Surface | What it is |
|---|---|
| Luma app | `app.lumalabs.ai` — browser + iOS, agentic workflows. Plans: Plus / Pro / Ultra; Enterprise for business |
| Luma API | `lumalabs.ai/api` — image ops via UNI-1.1, video ops via Ray3.2 including Multi-Keyframe and Reframe. Python and JS/TS SDKs. Tiers: Build (usage-based), Scale (dedicated capacity + SLA) |

## TODO before this leaves `status: draft`

- [ ] Pull duration + aspect-ratio enums from the API reference
- [ ] Confirm keyframe input format and timing semantics
- [ ] Record pricing/credit model well enough to say when Luma is the expensive choice
- [ ] Check for official Luma prompting guidance — vendors often publish a dialect
- [ ] Resolve the Ray3.2 vs Ray3.14 naming question (see `knowledge/research-queue.md`)
