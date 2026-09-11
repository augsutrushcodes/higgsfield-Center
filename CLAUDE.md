# CLAUDE.md

Instructions for Claude Code working **on** this repo. For working **with** the
skill, the entry point is root `SKILL.md`.

## Project

Higgsfield Center — a cross-platform Claude skill library routing AI
creative-generation work across Higgsfield, Luma, Beeble, and more over time.
Markdown skills plus one pure-stdlib Python validator. No build step.

## Layout

```
SKILL.md            root dispatcher — routing table, tie-breaks, load map, checklist
skills/<platform>/  one directory per platform, one SKILL.md each
skills/shared/      cross-platform craft (not a skill — a reference file)
skills/_template/   scaffold; exempt from the hfc- prefix and freshness checks
knowledge/          durable research; not loaded during normal skill use
scripts/validate.py the gate
workspace/          git-ignored: input/ → processed/, output/
```

## Commands

```bash
python3 scripts/validate.py           # health check
python3 scripts/validate.py --strict  # CI gate — warnings become failures
/validate                             # same, via slash command
```

## Rules

- **The pre-delivery checklist lives in root `SKILL.md` and only there.** Cite
  items by number from anywhere else. Never restate or renumber them — that's
  how a rule ends up written in four places with three of them stale.
- Every `skills/*/SKILL.md` needs frontmatter: `name`, `description`,
  `metadata.version`, `metadata.updated`, `metadata.status`, and — sub-skills
  only — `metadata.parent: higgsfield-center`. The root dispatcher must **not**
  declare a parent. `validate.py` enforces all of this.
- `tags` nests **inside** `metadata`, never at the top level.
- Sub-skill names use the **`hfc-` prefix**. This avoids a router collision
  with OSideMedia's upstream `higgsfield` skill when both are installed.
- Sub-skill `metadata.version` values are independent of each other and of the
  root. Don't sync them.
- Every platform directory on disk must be routed from the root `SKILL.md`
  table. `validate.py` reconciles disk against dispatcher.
- **No platform fact from memory.** Every factual claim carries a
  `> **Verified YYYY-MM-DD** — <url>` marker citing a primary source, or is
  marked `> **UNVERIFIED**` with what would confirm it. Anything over 30 days
  old is stale.
- Update `CHANGELOG.md` for user-facing changes.
- Run `python3 scripts/validate.py` before any commit touching `skills/`.

## Conventions

- QUICK FACTS blocks are routing aids, not the rules. Label them that way and
  link each line into the body.
- Split a platform file into named satellites in its own directory once it
  passes ~400 lines. A fat file that always loads in full is a context tax.
- Anti-bombast applies to this repo's own prose, not just to generated prompts.
  Demonstrate a rule with a bad-vs-plain rewrite; don't praise it.

Full rationale: `knowledge/skill-authoring-playbook.md`.
