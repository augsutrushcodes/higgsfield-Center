# Teardown — OSideMedia/higgsfield-ai-prompt-skill

**Source:** <https://github.com/OSideMedia/higgsfield-ai-prompt-skill>
**License:** MIT · **Author:** O-Side Media
**Version read:** v3.35.0 (repo updated 2026-08-22, specs snapshot 2026-08-07)
**Read on:** 2026-09-11 · shallow clone, full file tree + core docs read

This is a **standalone record**, not a pointer. The clone it was written from is
gone. Everything needed to rebuild the same architecture from scratch is here.

Nothing in this file is copied prose from that repo — it is a description of
structure, conventions and patterns. Their text stays theirs. See
[`../CREDITS.md`](../CREDITS.md).

---

## 1. What the repo is

A Claude **skill library** — not an app, not an SDK. ~5.5 MB, ~180 files, almost
all Markdown and JSON, with a small pure-stdlib Python tooling layer.

Its single job: turn a natural-language creative request into a
production-grade prompt for [higgsfield.ai](https://higgsfield.ai). It
deliberately **does not execute** the generation. Higgsfield ships its own CLI,
MCP connector and bundled skills for that. The repo states the boundary
explicitly and repeatedly: *this layer produces the prompt, their layer makes
the call, and this layer never shells out to theirs.*

That clean layer split is the single most reusable idea in the whole repo.

## 2. Top-level layout

```
SKILL.md                  root dispatcher — the entry point, routes to sub-skills
README.md                 public-facing overview + install + end-to-end example
CLAUDE.md                 instructions for Claude Code working ON the repo
DISCIPLINE.md             9 cross-cutting discipline patterns, 3 tiers
CONTRIBUTING.md           PR process + the validate.py gate
CHANGELOG.md              ~112 KB, every user-facing change, version-anchored
INDEX.md                  ~98 KB, GENERATED heading index of every SKILL.md
LICENSE                   MIT
.markdownlint.json        linter config
model-guide.md            video + image model comparison tables
image-models.md           image model specs, UI controls, pricing
vocab.md                  ~35 KB camera + cinematic vocabulary
prompt-examples.md        ~36 KB production examples, before/after pairs
photodump-presets.md      29 photodump style presets
production-benchmarks.md  iteration + cost + acceptance-rate anchors
requirements.txt          one real dep (fpdf2), everything else stdlib

skills/                   33 sub-skill dirs + shared/
templates/                10 genre + ad-asset-prep + character-design/6
                          + seedance/9 + text-overlays/3
specs/                    GENERATED machine-readable model specs + dated snapshots
scripts/                  9 Python tools
db/                       memory JSON + append-only generation ledger
docs/                     extended refs + archive/ + user-guide/
evals/                    behavioural eval cases + run_evals.py
tests/                    pytest suite for the Python tooling
workspace/                git-ignored working area: input/ processed/ output/
.claude/                  settings.json + rules/ (thin pointers) + commands/
.github/workflows/        validate.yml + spec-drift.yml
```

## 3. The dispatcher pattern (`SKILL.md`, 386 lines)

This is the architectural core. One file the agent always reads first, which
does six things in order:

1. **YAML frontmatter** — `name`, a long prose `description` listing every
   trigger phrase, `user-invocable: true`, and a `metadata` block
   (`tags`, `version`, `updated`, `author`, `license`).
2. **HARD RULES — a pre-delivery checklist** (8 numbered items). Framed as
   something the agent *runs before sending*, explicitly not as prohibitions
   stated once and forgotten. The named failure mode it exists to stop is
   **plausibility-over-verification**: producing output that looks right
   because the model's training knows the rough shape of the domain, rather
   than because it actually opened the files. Rule 1 forces a visible routing
   line as the first line of every response; rule 2 requires the routed files
   to have been genuinely *read*, and says grep snippets do not count.
3. **Working-folders contract** — `workspace/input/` → `workspace/processed/`,
   deliverables to `workspace/output/`, never the repo root. Uploads get
   *moved*, never deleted.
4. **Fast Path vs Full Path** — a default-and-go table for simple requests
   (16:9 / 8s / Cinematic / Kling 3.0 / Soul 2.0) vs a
   confirm-before-generating gate for production work, with an explicit
   anti-fragmentation rule: ask everything in one message.
5. **Routing table** — ~60 rows of `User wants → Route to`. Includes explicit
   **tie-break rows** for the pairs that genuinely collide (Soul vs
   character-design; Seedance 2.0 vs 2.5; Vibe Motion vs Motion Design), each
   with the disambiguating question to ask.
6. **Load map** — the routing table says *where*, the load map says *how much*.
   Ends with: "one routing-table row → that sub-skill; resist loading more than
   the row names." This is the context-budget control.

Then output format, the shared-resources table, and the sub-skill roster.

## 4. Sub-skill file contract

Every `skills/<name>/SKILL.md`:

- frontmatter requires `name`, `description`, `metadata.version`,
  `metadata.updated`, and — for sub-skills only — `metadata.parent: higgsfield`.
  The root dispatcher has no `parent`. `scripts/validate.py` enforces this.
- `tags` must be nested **inside** `metadata`, not at the top level.
- Sub-skill versions are **deliberately independent** of the root release
  version. CLAUDE.md explicitly warns not to "fix" them to match — newer
  surfaces sit at 1.x while legacy ones sit at 3.x, and the root frontmatter is
  the sole source of truth for the release number.
- Most open with a **QUICK FACTS** block: 5–8 one-line takeaways, each ending
  in a `[→](#anchor)` link into the body. Labelled as *routing aids, not the
  rules themselves*. `scripts/build_index.py` verifies those anchors resolve.
- Big sub-skills split into satellites in the same directory rather than
  growing unboundedly — e.g. `higgsfield-seedance/` carries `SKILL.md` plus
  `ENGINE-RULES.md`, `PRODUCTION-PATTERNS.md`, `HELL-GRIND.md`,
  `FAILURE-MODES.md`. The satellite is loaded on demand, named from the parent.

### The 33 sub-skills

| Sub-skill | Concern |
|---|---|
| `higgsfield-workspaces` | Which Higgsfield workspace/tool fits the job at all |
| `higgsfield-prompt` | Core MCSLA formula, prompt structure, identity/motion split |
| `higgsfield-image-shots` | Cinematic still framing, angles, composition |
| `higgsfield-gpt-image-2` | GPT Image 2.0 director (+2 workflow satellites) |
| `higgsfield-models` | Model selection (+ `MODELS-DEEP-REFERENCE.md`, 58 KB) |
| `higgsfield-camera` | Named camera controls |
| `higgsfield-motion` | Named motion + VFX presets |
| `higgsfield-style` | Visual styles, colour grades, lighting |
| `higgsfield-soul` | Soul ID character consistency |
| `higgsfield-character-design` | Pre-production: premise, world, story spine, visual DNA |
| `higgsfield-scene-engine` | Structural scene audit before spending credits |
| `higgsfield-apps` | One-click Apps |
| `higgsfield-recipes` | Genre scene templates |
| `higgsfield-troubleshoot` | Failed/poor generations, vision-grounded diagnosis |
| `higgsfield-assist` | Copilot, credits, plan selection, ledger read path |
| `higgsfield-mixed-media` | Artistic preset overlays |
| `higgsfield-moodboard` | Moodboards, Soul Hex, project-level consistency |
| `higgsfield-pipeline` | Multi-stage production chains |
| `higgsfield-canvas` | Node-based infinite-board workspace |
| `higgsfield-content-factory` | Campaign pipeline research→plan→generate→publish→report |
| `higgsfield-marketing-studio` | DTC ad presets, 4–15 s ad video |
| `higgsfield-recall` | Pre-generation memory check + ledger write path |
| `higgsfield-cinema` | Cinema Studio 2.5 / 3.0 / 3.5 (116 KB — largest file) |
| `higgsfield-seedance` | Seedance 2.0 director (99 KB + 4 satellites) |
| `higgsfield-seedance-2-5` | Seedance 2.5 omni-reference, 4 modes (+2 satellites) |
| `higgsfield-seedance-vfx` | Video-to-video footage transformation |
| `higgsfield-acting` | Performance craft, beats, subtext, eye life |
| `higgsfield-facs` | FACS Action Unit codes for facial expression |
| `higgsfield-shotlist-director` | Script → connected shotlist as editable HTML |
| `higgsfield-motion-design` | Animated ad as AI-rendered video |
| `higgsfield-vibe-motion` | Motion graphics as Remotion **code** |
| `higgsfield-stack` | Coexistence with the official CLI / MCP / bundled skills |
| `shared/negative-constraints.md` | Shared artifact-prevention reference |

## 5. The MCSLA formula

The repo's signature output contract. Five layers, every video prompt:

| Letter | Layer |
|---|---|
| **M** | Model |
| **C** | Camera |
| **S** | Subject |
| **L** | Look |
| **A** | Action |

Supporting rules: be specific and name actual presets; keep under 200 words in
the short-form regime; `Subject → Action → Camera → Style` is the most reliable
ordering. The 200-word cap has an explicit documented carve-out — long
block-scaffold production prompts swap the word cap for structural lint, and
the exception is written into the HARD RULE itself rather than left to
judgement.

## 6. The verification spine

The most transferable engineering idea in the repo. Platform facts are never
trusted from model memory:

- `specs/` holds **generated** machine-readable model specs (video, image,
  audio) in both JSON and YAML, each built from a **dated snapshot** of the
  platform's own model catalogue. Ten dated snapshots are committed, spanning
  2026-06-11 to 2026-08-07.
- `specs/` is marked *generated — never hand-edit*. `scripts/sync_specs.py`
  regenerates it from the newest snapshot; `scripts/validate.py` re-runs the
  generation and diffs, so a hand-edit or a generator change is caught.
- Specs carry a `snapshot_date`. Past **30 days** they are treated as stale and
  the agent is told to verify live instead of trusting the file.
- `scripts/refresh_specs.py` is a drift tripwire with a meaningful exit-code
  contract: `0` fresh, `3` changed, `1` pull failed, `4` the upstream CLI's
  shape changed. `--update-baseline` accepts a reviewed change.
- `.github/workflows/spec-drift.yml` runs it weekly. It ships **dormant on
  purpose** — it needs platform credentials as a repo secret before it does
  anything. Drift opens a GitHub issue; expired auth fails the job loudly.

The rule this serves, stated in the HARD RULES: aspect ratio is an *enum*, not
a free-form value. The worked example is that Seedance 2.0 supports native 21:9
and Kling 3.0 does not, and that "2.35:1 / anamorphic" is style vocabulary for
the Look line, never an output ratio.

## 7. The memory layer

- `db/filter-memory.json`, `db/quality-memory.json` — seeded failure memory.
- `db/ledger/<project>.json` — **append-only generation ledger**. Every attempt
  gets one row: kept, rejected, or filter-flagged. Corrections are *superseding
  rows*, never edits.
- Logging the denominator is the whole point: failure-only logging cannot
  produce a hit rate. With successes logged too, ~30–40 rows yields real
  takes-per-kept ratios per shot type instead of vibes.
- Tags and reject reasons come from **controlled vocabularies** defined in
  `db/ledger/README.md` — free text would make the data unaggregatable.
- The **5-second rule** governs adoption: at most one question and one command
  to write a row, never a form. Stated reason — if logging costs more attention
  than that, adoption dies by week two.
- `ratio` splits structural from stochastic rejections and flags low-sample
  rows rather than faking precision.
- `log-route` / `routing` record which sub-skills each request opens, so
  "which skills are load-bearing, which should retire" becomes a data question.
  Explicitly labelled **instrumentation, not a verdict** — a small sample is
  not evidence a skill is dead.

## 8. DISCIPLINE.md — 9 patterns in 3 tiers

Deliberately **3-3-3 symmetric**. Each pattern is stated, given a *when to
apply*, and — critically — pointed at a **concrete demonstration** already in
the codebase. Observed practice, not aspiration.

**Tier 1 — workflow:** pre-prompt confirmation gate · explicit-stop between
phases · inventory-extraction checklist before composing · iteration-is-craft ·
lock-before-generate · plausibility-over-verification · falsifiable success
criteria · log-every-generation

**Tier 2 — output:** visual-marker-only (describe by what is *visible*, never
proper names or unobservable attributes, because visual markers survive
regeneration) · triple-redundant runtime · single-variable iteration ·
systematic-vs-stochastic fork · vision-grounded diagnosis · BAD/GOOD/GREAT
gradients · skill-with-baked-context · anti-bombast

**Tier 3 — architectural:** 3-stage chain / 4-phase loop · closing-block baked
into every prompt · strict-order workflow refusing to skip phases ·
pre-delivery self-repair pass

Two entries stand out as unusually self-aware:

- **Systematic-vs-stochastic fork.** Single-variable iteration is only correct
  for a *systematic* miss — a prompt failing the same way every roll. At a
  ~1.5 % acceptance bar most misses are *stochastic variance*, and iterating on
  those "fixes" a prompt that was already right. So decide the fork first:
  structural rejects → iterate; stochastic → lock the prompt and batch-and-cull.
  The classification is computed from the ledger, not eyeballed.
- **Anti-bombast paradox.** The rule against marketing voice can itself slide
  into marketing voice about restraint. The stated fix is to *demonstrate* the
  rule with a bad-vs-plain rewrite rather than to praise it.

## 9. Tooling (`scripts/`, pure stdlib except the PDF generator)

| Script | Job |
|---|---|
| `validate.py` (48 KB) | The gate. Frontmatter contract, relative-path resolution, JSON schemas, version consistency across README badge + README footer + CHANGELOG top entry, dispatcher↔disk parity, spec regeneration diff, snapshot age, description coverage, INDEX/QUICK-FACTS anchors, ledger integrity. `--strict` turns SKIPs into failures. `--evals` runs the behavioural cases. |
| `higgsfield_memory.py` (72 KB) | Ledger + memory ops: `log-gen`, `amend-gen`, `ratio`, `budget`, `log-route`, `routing`, `stats` |
| `seedance_lint.py` (51 KB) | Preflight linter — catches illegal model/mode/resolution/ratio combos before credits burn |
| `sync_specs.py` | Regenerates `specs/` from the newest dated snapshot |
| `refresh_specs.py` | Live-vs-baseline drift tripwire |
| `build_index.py` | Regenerates `INDEX.md`, verifies QUICK FACTS anchors |
| `generate_user_guide.py` (79 KB) | Release PDF (the only third-party dep: `fpdf2`) |
| `validate_user_guide.py` | PDF drift check — text extract + binary diff |
| `sub_skill_descriptions.py` | Shared data module: canonical sub-skill roster |

### The release gate

Three commands, all green, before any release:

```
python3 scripts/validate.py --strict
python3 -m pytest tests/ -q
python3 scripts/validate.py --evals
```

A version bump needs a git tag and a GitHub release, not just a commit. `main`
is protected, so the *merge commit* gets tagged. The PDF is an untracked
release artifact uploaded to the release, never committed.

Commit format: `feat: vX.Y.Z — description` / `fix: vX.Y.Z — description`.

### CI

`.github/workflows/validate.yml` on every push and PR: strict validate, then a
**two-directional linter self-check** — it asserts the linter *fails* on two
known-illegal combos and *passes* on one known-good prompt, so a linter that
silently stopped working is caught. Then pytest, then evals.

## 10. Anti-duplication discipline

The HARD RULES have exactly **one canonical home** — root `SKILL.md`. CLAUDE.md
and DISCIPLINE.md both carry an explicit note saying they may *cite rules by
number* but must never restate or renumber them, and `validate.py` actively
checks the three surfaces for drift. `.claude/rules/*.md` are deliberately thin
pointers to the root reference files rather than copies.

This is the fix for the commonest rot in a docs-heavy repo: the same rule
written in four places, three of which go stale.

## 11. Install surfaces

- **Claude Code** — clone into `~/.claude/skills/<name>`
- **Claude Cowork** — drop the folder into the workspace; `SKILL.md` at the
  repo root is the dispatcher
- **Claude.ai Projects** — root `SKILL.md` as the instruction base, files from
  `skills/` as project documents

## 12. What to steal, and what not to

**Steal:**

- root dispatcher + routing table + load map (context budget control)
- frontmatter contract enforced by a validator, not by hope
- pre-delivery checklist framing instead of a prohibitions list
- one canonical home per rule + a drift check across surfaces
- dated snapshots with a staleness gate, and generated files that are diffed
  against a regeneration
- the append-only ledger with controlled vocabularies and the 5-second rule
- tie-break routing rows for genuinely colliding sub-skills
- QUICK FACTS blocks with verified anchors
- CI that tests the linter in both directions

**Don't steal yet:**

- the sheer volume. 33 sub-skills and a 116 KB file are the output of many
  months. Starting there produces stale files nobody reads.
- the PDF user-guide pipeline — two scripts and a release step for a
  deliverable most repos don't need.
- deep per-model prose before you have a verification spine. Without dated
  snapshots and a staleness gate, detailed model docs become confidently wrong
  within weeks — which is the exact failure the repo built `specs/` to prevent.
