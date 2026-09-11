---
name: hfc-beeble
description: >
  Use when the user asks about Beeble (beeble.ai, sometimes written "Beebl"),
  Beeble Studio, SwitchX, AI relighting, 3D Relight, VFX Pass Generator,
  PBR / alpha / depth passes, SDR-to-HDR conversion, background removal for
  compositing, the Beeble Canvas node graph, or Beeble's Nuke / Blender /
  Unreal plugins. Also use when the job is fixing or relighting footage that
  already exists rather than generating new footage.
metadata:
  tags: [beeble, vfx, relight, compositing, hdr, exr, nuke, blender, unreal]
  version: 0.1.0
  updated: 2026-09-11
  parent: higgsfield-center
  status: draft
---

# Beeble

> **Naming:** the site is **beeble.ai**. "Beebl.ai" is a common misspelling and
> should route here.

> **Verified 2026-09-11** — <https://beeble.ai> and <https://docs.beeble.ai>.

## QUICK FACTS

*Routing aids. Read the sections for the actual rules.*

- Beeble is a **VFX / post platform**, not a text-to-video generator. Its
  philosophy is "fix it in post" [→](#what-lane-this-is)
- Core lane: **relighting and compositing real footage** with per-pass control
  [→](#features)
- **SwitchX** is the video-to-video surface — change things in footage while
  preserving what matters [→](#features)
- **VFX Pass Generator** emits PBR, alpha and depth maps — the passes a real
  compositor expects [→](#features)
- **SDR→HDR** converts 8-bit footage to 16-bit EXR [→](#features)
- Two products: **cloud** (2K, no setup) and **Beeble Studio** desktop
  (4K, local, unlimited, offline pass generation) [→](#products)
- Plugins for **Nuke, Blender, Unreal**, plus an iPhone camera-tracking app —
  this is a pipeline tool, not a closed box [→](#integrations)
- Audience is VFX artists and indie filmmakers who need pixel-level control and
  professional export formats, not social-first creators [→](#what-lane-this-is)

## What lane this is

The important routing fact: **Beeble does not compete with Higgsfield or Luma.**
Those generate footage. Beeble takes footage — real or generated — and gives it
production finishing: relight it, composite into it, pull the passes, take it
to 16-bit.

That makes it a **downstream** entry in this library. It usually appears at the
*end* of a chain, not as an alternative to one.

```
generate (Higgsfield / Luma)  →  finish (Beeble)  →  grade / edit
shoot on camera               →  finish (Beeble)  →  grade / edit
```

Route **to** Beeble when the user says: relight, match the lighting, change the
time of day, composite, pull a matte, key this, I need depth/alpha, get me
EXRs, put this person in that environment, fix it in post.

Route **away** when the user has no source footage. Beeble's starting point is
a plate.

## Products

| Product | Resolution | Processing | Notes |
|---|---|---|---|
| Beeble (cloud) | 2K | hosted | No setup; all AI models + SwitchX |
| Beeble Studio (desktop) | 4K | local, unlimited | Offline VFX Pass Generator |

The desktop/local split matters for client work with footage that can't be
uploaded. Flag it when confidentiality comes up.

## Features

| Feature | What it does |
|---|---|
| **Canvas** | Node-graph editor for composing AI VFX pipelines |
| **SwitchX** | Video-to-video — switch elements in footage while preserving the rest |
| **Background Remover** | AI alpha matte extraction from image or video |
| **VFX Pass Generator** | Generates PBR maps, alpha, and depth |
| **3D Relight** | Real-time relighting with physically-based rendering |
| **SDR to HDR** | 8-bit SDR footage → 16-bit HDR EXRs |

The node-graph shape is worth noting: it composes, which means Beeble work is
naturally a *pipeline* of named stages rather than a single prompt. That fits
the stage-artifact-handoff pattern in the
[playbook](../../knowledge/skill-authoring-playbook.md) better than a
prompt-per-shot model does.

## Integrations

Plugins for **Nuke**, **Blender**, and **Unreal Engine**, plus an **iPhone
camera app for tracking**.

The iPhone tracking app is the interesting one — it means camera solve can come
from a phone rather than a tracked shoot, which is the actual enabler behind the
"virtual production for indie filmmakers" positioning.

## Handoff with the generation platforms

The 16-bit HDR / EXR overlap is not a coincidence and is worth getting right:

- **Luma Ray3.2** already outputs native 16-bit HDR with ACES2065-1 EXR. Footage
  from there arrives in Beeble already in a gradeable colour space — no SDR→HDR
  step needed.
- **SDR-only sources** (most generated video, most phone footage) need Beeble's
  SDR→HDR pass before they'll hold up to a relight or a grade.

So: check the source's colour depth before recommending the conversion pass.
Running SDR→HDR on footage that is already 16-bit is wasted work.

## TODO before this leaves `status: draft`

- [ ] Read `docs.beeble.ai/llms.txt` for the full documentation index
- [ ] Get exact node names in Canvas, and the pass names the generator emits
- [ ] Record supported input codecs / containers and any clip-length limits
- [ ] Confirm whether there is an API or CLI surface, or plugins only
- [ ] Pricing / plan structure for cloud vs Studio
- [ ] Write one worked end-to-end example: generated clip → relight → graded EXR
