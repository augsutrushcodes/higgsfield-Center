---
name: hfc-PLATFORM
description: >
  Use when the user asks about PLATFORM — list the real trigger phrases here,
  including product names, model names, feature names, and common misspellings.
  This description is what the router matches on, so vague wording here becomes
  wrong routing later.
metadata:
  tags: [platform, lane, keywords]
  version: 0.1.0
  updated: YYYY-MM-DD
  parent: higgsfield-center
  status: draft
---

# PLATFORM

> **Verified YYYY-MM-DD** — <primary source URL>
>
> Replace this with the real source. Vendor docs, changelog or pricing page —
> not a review site, not a video summary, not model memory.

## QUICK FACTS

*Routing aids. Read the sections for the actual rules.*

- Five to eight one-line takeaways, each linking into the body [→](#what-lane-this-is)
- Lead with the thing this platform does that nothing else on the list does
- Hard limits belong here: max duration, resolution ceiling, reference count
- If a fact isn't verified yet, say so here rather than omitting it

## What lane this is

Generate / edit / relight / finish / audio — pick one and say it plainly.

The important routing question is not "what can it do" but "when is it the
right call and when is it the wrong one." Write both.

## Models / products

| Name | What it does | Key limits |
|---|---|---|
| | | |

> **UNVERIFIED** — anything not yet confirmed from a primary source goes in a
> block like this. An honest TODO is fine; a silent guess is not.

## When to pick it

Route **to** this platform when:

-

Route **away** when:

-

## Hard limits

The values that cost money when wrong. Get these exactly right:

- Duration: **enum or range?**
- Resolutions:
- Aspect ratios: **enum — list them**
- Reference inputs accepted, and how many:

## Workflow

Numbered stages, each producing something the next stage consumes. If the
platform has a cheap draft mode, stage one is always "use it."

1.
2.

## Surfaces

| Surface | What it is |
|---|---|
| | |

## Cross-platform handoff

How output from here enters another platform, and what has to be true first
(colour space, codec, resolution). This is where cross-platform work actually
breaks.

## TODO before this leaves `status: draft`

- [ ] Duration and aspect-ratio enums from a primary source
- [ ] Pricing / credit model — enough to say when this is the expensive choice
- [ ] Official prompting guidance, if the vendor publishes a dialect
- [ ] One worked end-to-end example
- [ ] Add a routing row to the root `SKILL.md`, or `validate.py` will flag it
