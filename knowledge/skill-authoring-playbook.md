# Skill-Authoring Playbook

How to grow this repo into a skill worth publishing. Distilled from the
[teardown](higgsfield-ai-prompt-skill-teardown.md), reordered as *what to do
next* rather than *what they did*.

Read this before adding a platform.

---

## The one rule that matters most

**Never write a platform fact from memory.**

A model's training data knows the *rough shape* of every AI creative tool —
that there are aspect ratios, that there are durations, that flags look
roughly like `--aspect-ratio`. That is exactly enough knowledge to produce
something plausible and wrong, and a wrong model name or an illegal enum costs
real credits.

So every factual claim in this repo carries provenance:

```markdown
> **Verified 2026-09-11** — <https://lumalabs.ai/llm-info>
```

and anything not yet checked is marked, loudly:

```markdown
> **UNVERIFIED** — needs a primary source before this is used in a prompt.
```

`scripts/validate.py` counts unverified blocks and reports them. It does not
fail on them — an honest TODO is fine, a silent guess is not.

## Dated snapshots beat prose

When you do verify something volatile (a model lineup, pricing, duration
enums), write the date next to it. Anything older than **30 days** is treated
as stale: re-check before relying on it. This is the cheap version of the
reference repo's generated `specs/` layer, and it buys most of the same
protection.

## Structure: dispatcher + thin platform skills

```
SKILL.md              one router everyone reads first
skills/<platform>/    one directory per platform, one concern each
skills/shared/        cross-platform craft that would otherwise be copy-pasted
knowledge/            durable research; not loaded during normal use
```

The dispatcher does three jobs and no more:

1. **Route** — a `User wants → Route to` table. Add a **tie-break row** for any
   two entries that genuinely collide, with the disambiguating question spelled
   out. Colliding routes are the #1 cause of a skill picking the wrong file.
2. **Budget** — a load map saying *how much* to read. Without it an agent opens
   everything and burns context on files it didn't need.
3. **Gate** — a short pre-delivery checklist the agent runs *before* replying.

## Write rules as a pre-delivery checklist

A list of prohibitions gets read once and forgotten. A checklist framed as
"confirm these before sending" gets run. The difference is whether the rule
fires at the moment it's needed.

Keep it short — under ten items — and give each one a failure it prevents.
A rule with no named failure mode is decoration.

## One canonical home per rule

Write each rule in exactly one file. Everywhere else, **cite it by number**.

The standard rot in a docs-heavy repo is the same rule written in four places,
three of which drift. The reference repo fixes this by declaring a canonical
home and having its validator diff the surfaces. Do the same from day one —
it costs nothing now and is painful to retrofit.

## Sub-skill file contract

Every `skills/<name>/SKILL.md` opens with:

```yaml
---
name: hfc-<platform>
description: >
  Use when ... (spell out the trigger phrases — this is what the router matches)
metadata:
  tags: [...]
  version: 0.1.0
  updated: YYYY-MM-DD
  parent: higgsfield-center
  status: draft | verified | stale
---
```

Then a **QUICK FACTS** block — five to eight one-line takeaways, each linking
to the section that actually holds the rule. Label it as a routing aid so
nobody mistakes the summary for the source.

`scripts/validate.py` enforces the frontmatter contract, checks that
`parent` matches, that every platform on disk is routed from the dispatcher,
and that relative links resolve.

## Split before a file gets fat

When a platform skill outgrows roughly 400 lines, split the overflow into a
named satellite in the same directory (`VFX-PIPELINE.md`, `FAILURE-MODES.md`)
and have `SKILL.md` point at it. Loaded on demand, named from the parent. One
40 KB file that always loads in full is a context tax on every request.

## Describe by visible markers

For any generation prompt: describe subjects by what a camera can *see* —
clothing, build, posture, hair, what they're doing. Not proper names, not ages,
not backstory. Visual markers survive a regeneration; "Sarah, 34, recently
divorced" does not render.

## Change one variable per iteration — but check the fork first

Single-variable iteration only diagnoses a *systematic* miss: the prompt is
genuinely wrong and fails the same way every time. When acceptance rates are
low, most misses are *stochastic variance*, and iterating on those quietly
"fixes" a prompt that was already correct.

So: structural, repeatable failure → iterate one variable. Random, different
every time → lock the prompt and run a batch, then cull against criteria you
wrote down *before* generating.

## Anti-bombast, applied to itself

Replace `epic`, `cinematic masterpiece`, `ultra realistic` with named physical
mechanisms — `low-angle 35 mm medium shot`, `warm practical key from
screen-left`. Adjectives describe what the output should *be*; mechanisms
describe what the prompt should *do*.

And the same register applies to this repo's own prose. Documentation that
explains avoiding marketing voice can easily become marketing voice about
restraint. Demonstrate with a bad-vs-plain rewrite; don't praise the rule.

## Ship with a gate

`python3 scripts/validate.py` before every commit that touches `skills/`.
It's cheap and it's what keeps a growing library from rotting. Add checks as
you find failure modes — the validator is where lessons accumulate.

## Growth order

1. Dispatcher + one platform you actually use daily. Nothing else.
2. Use it for real work for a week. Note every time it routes wrong or you
   have to correct it.
3. Fix routing from those notes. Only then add platform two.
4. Add `skills/shared/` the moment you catch yourself copy-pasting between two
   platform files — not before.
5. Add a memory/ledger layer only once you have enough volume for ratios to
   mean anything. Below ~30 logged results it's overhead with no payoff.

Volume is the output of months of real use, not a starting condition. Thirty
sub-skills written in a weekend are thirty stale files.
