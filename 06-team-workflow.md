# SDD in a Distributed Team

> **Solo SDD is interesting. Team SDD is where the value compounds.**
>
> The 25-min demo shows the single-developer loop. This file shows what changes when you have multiple features, multiple humans, and AI agents working in parallel against the same repo.

## The mental shift

In vibe coding, the unit of work is a **prompt**. It vanishes after the response. Review happens on the resulting code — usually 500+ lines, often days later, by someone who wasn't in the conversation.

In Spec-Driven Development, the unit of work is an **artifact**: `spec.md`, `plan.md`, `tasks.md`. Each one is short, readable, and lives in a PR before any code is written. Review happens **three times**, on cheap and small artifacts, instead of once on expensive and large code.

```mermaid
flowchart LR
    subgraph Vibe["🌀 Vibe Coding"]
        V1[Prompt] --> V2[500-line PR] --> V3[Review<br/>too late]
    end

    subgraph SDD["📐 Spec-Driven"]
        S1[Spec PR<br/>~50 lines] --> S2[Plan PR<br/>~80 lines] --> S3[Tasks PR<br/>~30 lines] --> S4[Code PR<br/>mostly mechanical]
    end

    style V3 fill:#ffe1e1,stroke:#d32f2f
    style S1 fill:#e1f5ff,stroke:#0288d1
    style S2 fill:#fff4e1,stroke:#f57c00
    style S3 fill:#fff4e1,stroke:#f57c00
    style S4 fill:#e1f5d3,stroke:#388e3c
```

## Multiple features, in parallel, no merge conflicts

SpecKit scaffolds each feature into its own folder:

```
.specify/
├── memory/
│   └── constitution.md                ← ONE per repo, shared across features
└── specs/
    ├── 001-url-shortener/             ← Dev A's feature
    │   ├── spec.md
    │   ├── plan.md
    │   └── tasks.md
    ├── 002-user-profiles/             ← Dev B's feature, in parallel
    │   ├── spec.md
    │   ├── plan.md
    │   └── tasks.md
    └── 003-rate-limiting/             ← AI agent's feature, in parallel
        ├── spec.md
        ├── plan.md
        └── tasks.md
```

**Why this matters:** spec/plan/tasks files live in disjoint folders. Three developers can run `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement` on three different features at the same time **without ever touching the same file**. Merge conflicts in SpecKit artifacts are nearly impossible by construction.

The only shared artifact is `constitution.md` — and you change that rarely.

## Roles map to artifacts

The five commands aren't five steps for one person. They're a hand-off chain that maps naturally to team roles:

```mermaid
flowchart TD
    PM[👤 Product / PM<br/>knows the user] -->|writes| Spec["📋 spec.md<br/>(what &amp; why)"]
    Spec -->|PR review| SpecOK{Spec approved?}
    SpecOK -->|✅| TL[👩‍💻 Tech Lead<br/>knows the stack]
    TL -->|writes| Plan["🛠 plan.md<br/>(how)"]
    Plan -->|PR review| PlanOK{Plan approved?}
    PlanOK -->|✅| Senior[👨‍💻 Senior Dev<br/>knows the codebase]
    Senior -->|generates| Tasks["✅ tasks.md<br/>(ordered steps)"]
    Tasks -->|"/speckit.taskstoissues"| GH["🎫 GitHub Issues<br/>(one per task)"]
    GH -->|claimed by| Workers[👥 Devs<br/>+ AI agents]
    Workers -->|"/speckit.implement"| Code["💻 Code PR"]
    Code -->|PR review| Merged([✅ Merged to main])

    style Spec fill:#e1f5ff,stroke:#0288d1
    style Plan fill:#fff4e1,stroke:#f57c00
    style Tasks fill:#fff4e1,stroke:#f57c00
    style GH fill:#f5e1ff,stroke:#7b1fa2
    style Code fill:#e1f5d3,stroke:#388e3c
    style Merged fill:#e1f5d3,stroke:#388e3c,stroke-width:3px
```

You don't need separate humans for each role — but the artifacts make the hand-off explicit. Even when one person plays all roles, putting on the "product hat" for `spec.md` and the "tech lead hat" for `plan.md` produces better thinking than mashing both concerns into a single prompt.

## What each PR review actually checks

| Artifact | Reviewer asks | Cheap to fix here? |
|----------|---------------|---------------------|
| `constitution.md` (rare) | Do these principles match how we want to build? | ✅ trivial — change words in one file |
| `spec.md` | Did we get the user story right? Did we forget edge cases? | ✅ minutes |
| `plan.md` | Why this stack? Does it respect the constitution? Are there cheaper alternatives? | ✅ minutes |
| `tasks.md` | Is the dependency order correct? Are tasks small enough to assign individually? | ✅ minutes |
| Code PR | Does the implementation match the tasks? Did anything sneak in? | 🔴 expensive — refactor or revert |

**The economic argument:** finding a wrong assumption in `spec.md` costs 10 minutes of rewriting. Finding the same wrong assumption in a 500-line code PR costs a day. SDD frontloads cheap review.

## AI agents as teammates

GitHub Copilot's cloud coding agent can pick up GitHub issues you tag for it. The workflow:

1. Human writes spec → PR → merge.
2. Human (or AI) writes plan → PR → merge.
3. `/speckit.taskstoissues` creates one issue per task.
4. Label an issue `copilot` (or assign to the Copilot bot user). The cloud agent claims it, **reads spec.md + plan.md + the task description** for context, branches off, implements **just that task's scope**, and opens a PR.
5. Human reviews the code PR (which is small, because it implements one task).

> ⚠ **Note on `/speckit.implement` vs the per-issue flow.** The two are alternative paths, not sequential:
> - `/speckit.implement` (single-developer flow) reads `tasks.md` and works through **all** tasks in one local session. There is no per-task mode built in.
> - `/speckit.taskstoissues` + cloud agent (team flow) is the **distributed** counterpart: each issue is implemented individually, in parallel, by whoever picks it up. The cloud agent does **not** run `/speckit.implement` per issue — it implements the issue's task directly using spec/plan as context.

AI becomes a **junior dev who works async**. You assign work to it the same way you assign work to a human — through issues with clear context. The spec/plan/tasks chain *is* the context.

> **CLI variant:** the same `/speckit.*` commands run 1:1 in the GitHub Copilot CLI. A team member who lives in the terminal hands off the same way; the artifacts don't care which client wrote them.

## FAQ — `/speckit.taskstoissues` deep dive

Audience asks this every time. The honest answers:

### Why bother? `tasks.md` is already in git.

Because `tasks.md` is a private Markdown list. **Issues are first-class GitHub objects.** Four concrete upgrades:

| Capability | `tasks.md` alone | After `/speckit.taskstoissues` |
|---|---|---|
| Assign to a specific developer | ❌ (just a checkbox in markdown) | ✅ assignee, label, project board |
| Cloud-agent handoff (async, parallel) | ❌ | ✅ label `copilot` → cloud agent picks up |
| PR auto-close via `Closes #42` | ❌ | ✅ link establishes traceability |
| Comment thread + decisions over time | ❌ | ✅ issue body + comments + reactions |

The biggest win is the **cloud-agent handoff**: after `/speckit.taskstoissues`, the entire backlog can be worked **in parallel, asynchronously**, by Copilot's cloud agent or by human teammates — instead of single-threaded inside one local `/speckit.implement` session.

> ⚠ **Important: `/speckit.implement` does NOT read GitHub issues.** Verified against the current upstream prompt at `templates/commands/implement.md` — step 3 is literally *"REQUIRED: Read tasks.md for the complete task list"*. Issues never appear. The two are **alternative paths**, not a chain:
>
> - **Local single-dev path:** `/speckit.implement` → reads `tasks.md` → implements **all** tasks in one session → ticks `[X]` in tasks.md.
> - **Distributed team path:** `/speckit.taskstoissues` → developers/cloud-agent pick up issues individually → each implements **one task** using spec.md + plan.md + the issue body as context. No `/speckit.implement` per issue — the per-issue work is done directly.

### How does it actually work under the hood?

The `/speckit.taskstoissues` prompt is ~10 lines:

1. Read `tasks.md` from the active feature folder.
2. Read `git config --get remote.origin.url`; verify it is a GitHub URL.
3. For each task, call the **GitHub MCP server's `issue_write` tool** to create one issue in that repo.
4. Hard safeguard: **never** create issues in a repo that doesn't match the local remote.

That is the whole mechanism. No magic.

### Is there a back-reference from `tasks.md` to the created issues?

**Out of the box: no.** The prompt only writes *forward* (tasks → issues). `tasks.md` stays unchanged after the command runs. The issue *body* typically contains the task description (because the model has the task text in context) but there is no programmatic guarantee.

Three patterns teams add themselves:

| Pattern | How | Effort |
|---|---|---|
| **Naming convention** | Add to the prompt: *"prefix every issue title with the T-number"*. Then `gh issue list \| grep "^T0"` maps cleanly back. | 5 sec extra prompt |
| **Follow-up prompt** | Right after `/speckit.taskstoissues`: *"Now update tasks.md and add the GitHub issue number in parentheses next to each task title."* The model still has the issue numbers in context. | 30 sec |
| **Forked prompt file** | Edit `.github/prompts/speckit.taskstoissues.prompt.md` in your repo, append a step 5: *"append a markdown table to tasks.md mapping T-number ↔ issue URL"*. Versionable in git, team-wide enforced. | 10 min, one-time |

**Demo zinger** if asked live: *"Out-of-the-box it's a one-way mapping. Want the round-trip? Fork the prompt file or chain a follow-up. That flexibility is exactly the point of SpecKit being just markdown prompts in `.github/prompts/` — you change behavior with a PR, not a release."*

## Constitution evolution

The constitution captures team agreements: "we use Postgres, not SQLite", "all endpoints need tests", "no client-side rendering", etc.

When team agreements change:

1. Open a PR that edits `.specify/memory/constitution.md`.
2. Discuss. Merge.
3. **The next feature's `/speckit.plan` automatically respects the new rules.**

Old features keep their old plan.md unless someone regenerates them. That's fine — the constitution is forward-looking guidance, not retroactive law.

## A week in the life (concrete example)

**Monday — Product writes specs.**
- PM opens 3 PRs, one per feature, each containing only `spec.md` for `001-url-shortener`, `002-profiles`, `003-rate-limit`.
- Tech Lead reviews each spec, suggests one edge case. PRs merged by noon.

**Tuesday — Tech lead writes plans.**
- Tech Lead runs `/speckit.plan` against each spec. Opens 3 PRs, one per `plan.md`.
- Devs review the plans, raise one question about whether `001` should use Redis. Discussion → no, sqlite. PRs merged.

**Wednesday — Senior dev generates tasks + routes to GitHub issues.**
- Runs `/speckit.tasks` on each feature.
- Runs `/speckit.taskstoissues` — 30 GitHub issues materialize, pre-assigned with context.
- 12 issues labelled `ai-implement` get picked up by Copilot's cloud agent overnight.

**Thursday — Code PRs land.**
- 12 PRs from the AI agent (small, one task each).
- 8 PRs from human devs.
- Each PR reviewed against `tasks.md` — does the diff match the task description? Mostly yes, takes ~5 min each.

**Friday — features merge.**
- All 3 features merge to main.
- PM uses the same `spec.md` files as release notes (they're already user-facing language).

## Anti-patterns to avoid

❌ **Skipping the constitution.** Without it, every feature picks its own stack and your codebase becomes a museum of trends.

❌ **Writing spec + plan + tasks in one prompt.** You lose the review checkpoints. Each one's value is being challengeable on its own.

❌ **Letting `/speckit.implement` run on un-reviewed tasks.** The tasks file is the contract between the team and the agent. Skip review and you get the same vibe-coded chaos, just routed through an extra file.

❌ **Treating the constitution as immutable.** It's a markdown file. PR it. Discuss. Update. Teams that never touch it eventually disagree with it silently.

❌ **Hiding the artifacts from non-engineers.** Specs are human-readable. Show them to PMs, designers, support. They'll catch product errors engineers miss.

## What stays the same as the 25-min demo

Everything technical. Same five commands. Same artifacts. Same constitution-driven discipline. The only change is **who** runs each command and **where** the artifact gets reviewed.

> The single-dev demo is a microcosm. The team workflow is the same loop, just unfolded across people and time.
