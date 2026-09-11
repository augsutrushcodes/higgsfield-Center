# Shared Prompt Craft

Cross-platform discipline. Applies wherever a prompt drives a generative
render, regardless of vendor. Platform files cover dialect; this covers craft.

---

## Describe by visible markers

Describe subjects by what a camera can see: clothing, build, posture, hair,
what the hands are doing. Not proper names, not ages, not backstory.

Visual markers survive a regeneration. "Sarah, 34, recently divorced" renders
nothing — the model has no pixels for it, so it invents some.

**Bad:** Sarah, a 34-year-old lawyer, looks regretful.
**Good:** A woman in a charcoal suit, collar loose, stands very still and looks
past the camera; her jaw is set and she doesn't blink.

## Decompose emotion into mechanism

A generic emotion word is an instruction the model can't follow. Break it into
observable behaviour: breath, eyes, jaw, shoulders, hands, weight, stillness.

"Sad" is a label. "She holds a breath a beat too long before answering, eyes
wet but not spilling" is a render.

## Anti-bombast

Replace `epic`, `beautiful`, `cinematic masterpiece`, `ultra realistic`,
`dramatic` with named physical mechanisms:

- `low-angle 35 mm medium shot`
- `warm practical key from screen-left, hard shadow on the back wall`
- `handheld, slight drift, breathing on the frame edge`

Adjectives describe what the output should *be*. Mechanisms describe what the
prompt should *do*. Only one of those is actionable.

## One primary action per clip

One primary action, one or two secondary at most. Multi-action prompts get
averaged into mush, and when one part fails you can't tell which.

## Image-to-video: describe only what changes

The source frame already contains the subject, the set, the lighting, the
composition. Re-describing them fights the conditioning. Say what *moves* and
what *changes* — nothing else.

Same rule for video-to-video: the source's camera move and subject are what
you're preserving. Name the transformation, not the plate.

## Aspect ratio is an enum

Per model, always. Not a free-form value, and not transferable between
platforms — one vendor's native 21:9 is another's hard no.

And keep the two vocabularies apart: `2.35:1`, `2.39:1`, "anamorphic" are
**style register** describing a look. They are not output ratios. Writing one
into an output-spec field is the single most common cross-platform mistake.

## Lock before you generate

Decide subject, camera, lighting and coverage *before* prompting, not during.
Decisions made inside the iteration loop drift from the original intent;
decisions made before it act as anchors the loop tests against.

## Write falsifiable criteria first

Before generating, write down what would make the result a reject. Specific
enough to check against the frame.

Without this the loop has no stopping condition, and every result gets
rationalised as good enough because no test was ever committed to.

## Iterate one variable — after checking the fork

Single-variable iteration only diagnoses a **systematic** miss: the prompt is
genuinely wrong and fails the same way every roll.

When acceptance rates are low, most misses are **stochastic variance**. Serial
iteration on those quietly "fixes" a prompt that was already right, and the
apparent improvement is just the next roll landing better.

So decide the fork before touching the prompt:

| Failure looks like | Do this |
|---|---|
| Same defect every roll — structural | Change **one** variable, re-roll |
| Different defect every roll — random | **Lock the prompt**, batch, cull against your criteria |

## Iteration is the work

Production-grade generative work runs at low acceptance rates. The rejected
takes are the craft, not evidence of failure. Budget for them up front —
treating each reject as a setback is how a project dies in week one.

## Log the denominator

If you log only failures you can never compute a hit rate. Log kept results
too, or the record can't answer the one question worth asking: how many takes
does this kind of shot actually cost?

Keep the write cheap — one line, controlled vocabulary for tags and reject
reasons. Anything heavier than that stops getting written by week two, and a
half-kept log is worse than none.
