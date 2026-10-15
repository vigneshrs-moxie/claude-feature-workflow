# Claude feature workflow

Skills and worker agents for [Claude Code](https://claude.com/claude-code) that take a feature or bug from a one-line request to reviewed pull requests, with a human sign-off at every stage.

You talk to one **Foreman** (the `/feature` skill). It hands each stage to a worker agent, checks the result against the files on disk, and gives you a short brief to approve before anything moves on. The [Feature Workshop](https://github.com/vigneshrs-moxie/feature-workshop) dashboard shows these jobs in a browser; it needs this workflow installed.

## Install

You need Claude Code installed and logged in (`claude` works in your terminal).

```sh
git clone https://github.com/vigneshrs-moxie/claude-feature-workflow.git
cd claude-feature-workflow
./install.sh
```

The script links `skills/*` into `~/.claude/skills/` and `agents/*.md` into `~/.claude/agents/`. Anything already there with the same name is moved aside as `<name>.bak`. Because they are links, `git pull` updates them in place. Set `CLAUDE_DIR` to install somewhere other than `~/.claude`.

Then in Claude Code, inside the repository you work on:

```
/feature Add a "Download CSV" button to the invoices page
```

## What is in here

### Skills (`skills/`)

| Skill | What it does |
|---|---|
| `feature` | The Foreman. Runs spec → investigate → plan → build → test → review → PRs through the agents below, one brief per stage. Also holds the rules every worker follows, the job options (how much process a job gets), the git workflow summary, and the review checklists. |
| `feature-spec` | Drafts a product spec from a request and recommends the small or large route. Holds `workflow-gates.md`, the rules for what each stage needs before it may start. |
| `feature-refine` | The detailed product interview for a large feature, one question at a time. |
| `feature-investigate` | Read-only look at how the repository behaves today, written up as private findings. |
| `feature-plan` | The implementation plan and test plan, from the spec and findings. |
| `review-walkthrough` | Builds a one-page cue sheet for an in-person review of a branch or PR. Changes are sorted into four zoom levels (System, Module, Function, Line); Quick shows only the highest level with changes, with Explain jumps to a short before/now explanation, and a view picker shows all levels or any one. A wrap-up collects follow-ups. |

### Agents (`agents/`)

Each file sets a worker's model, effort and tools. The Foreman dispatches them; you never call them directly.

- **Writers:** `feature-spec-writer`, `feature-investigator`, `feature-planner`, `feature-implementer`, `feature-tester`.
- **Review lenses**, run in parallel on the finished code: `feature-reviewer` (spec conformance), and `feature-review-permissions`, `-db`, `-tests`, `-ui`, `-errors`, `-performance`, `-conventions`.
- **`feature-fable-check`:** a short, independent second look at one document or change, on request.

## How a job runs

1. **Spec.** The Foreman drafts a spec and asks at most three questions.
2. **Route.** Each job gets a level of process, from a gate-free tweak to a full panel review. The Foreman suggests one from the request and the code it touches; you confirm or change it. Risky changes (migrations, auth, scoping, email) always get more review.
3. **Investigate and plan.** Read-only findings, then a plan you approve before any code is written.
4. **Build.** A fresh implementer per plan step, one local commit per step, in its own git worktree.
5. **Test and review.** The test plan runs; review lenses report; fixes get one round by default.
6. **PRs.** Pushed to your fork only. Pull requests to the organisation repository are opened only when you say so.

Every job keeps its own private folder under `~/.claude/feature-work/<slug>/` with the spec, findings, plan, briefs and a `status.json` the dashboard reads. Nothing from that folder is committed to the repository you are working on.

## Adapting it

- `skills/feature/git-workflow.md` and `skills/feature-spec/workflow-gates.md` describe one team's remotes, branch naming and PR stages. Edit them for yours.
- `skills/feature/checklists/` holds the review checklists per area (API, database, email, UI). Add your own.
- Model choices live in each agent's front matter.
