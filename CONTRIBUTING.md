# Contributing

This is a Claude skill library. Contributions are welcome — especially platform
research backed by primary sources.

## The one hard requirement

**Every factual claim needs provenance.**

A model's training knows the rough shape of every AI creative tool. That's
enough to write something plausible and wrong, and wrong facts here cost real
credits downstream. So:

```markdown
> **Verified YYYY-MM-DD** — https://vendor.example/docs
```

A primary source means the vendor's own docs, changelog, API reference or
pricing page. Not a review site, not a YouTube summary, not recollection.

If you can't verify something but it's worth recording:

```markdown
> **UNVERIFIED** — needs the API reference to confirm the duration enum.
```

An honest gap is useful. A confident guess is not.

## Adding a platform

1. Copy `skills/_template/SKILL.md` → `skills/<platform>/SKILL.md`
2. Work the intake checklist in `knowledge/research-queue.md`. The last item is
   the real test: **what does this platform do that nothing else on the list
   does?** If that can't be answered, it doesn't need a skill file.
3. Fill the template. Keep `status: draft` until the TODO list is clear.
4. Add a routing row to root `SKILL.md` — plus a **tie-break row** if it
   collides with something already routed. Colliding routes are the main cause
   of a skill opening the wrong file.
5. `python3 scripts/validate.py`
6. Update `CHANGELOG.md`.

## Changing an existing skill

- Bump `metadata.version` and `metadata.updated` in that file's frontmatter.
- Sub-skill versions are independent — don't sync them to each other or to the
  root.
- Refresh the `**Verified**` date only if you actually re-checked the source.
  Bumping the date without re-verifying is worse than leaving it stale, because
  it launders a guess into a fact.

## Style

- Name mechanisms, not adjectives. `low-angle 35 mm medium shot`, not
  `cinematic`. This applies to the repo's own prose too.
- Demonstrate a rule with a bad-vs-plain rewrite rather than praising it.
- QUICK FACTS blocks are routing aids — label them that way and link each line
  into the body that holds the actual rule.
- One concern per file. Split past ~400 lines into a named satellite in the
  same directory.
- Don't restate the pre-delivery checklist. It lives in root `SKILL.md` and
  only there; cite items by number.

## Before opening a PR

```bash
python3 scripts/validate.py
```

CI runs the same check plus a self-check asserting the validator still fails on
known-bad input. Describe what changed and why, and name your sources.

## License

Contributions are MIT licensed, same as the repo.
