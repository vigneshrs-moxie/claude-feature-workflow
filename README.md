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

The script does three things:
- Links `skills/*` into `~/.claude/skills/` and `agents/*.md` into `~/.claude/agents/`. Because they are links, `git pull` here updates them in place.
- Moves anything already there with the same name to `~/.claude/backups/claude-feature-workflow/<date>/`, outside the skills folder so Claude Code doesn't load it twice.
- Clones the [git workflow docs](https://github.com/vigneshrs-moxie/moxie-portal-git-workflow) to `~/Projects/moxie-portal-git-workflow`, or updates them if already cloned. The Foreman reads them before any branch or PR step. Keep that location; the skills look for it there.

Run it again after every `git pull`. Set `CLAUDE_DIR` to install somewhere other than `~/.claude`.

Then in Claude Code, inside the repository you work on:

```
/feature Add a "Download CSV" button to the invoices page
```

## What is in here

### Skills (`skills/`)

| Skill | What it does |
|---|---|
| `feature` | The Foreman. Runs clarify → spec → screens → investigate → plan → build → test → review → PRs through the agents below, one brief per stage. Also holds the rules every worker follows, the job options (how much process a job gets), the git workflow summary, and the review checklists. |
| `feature-spec` | Drafts a product spec from a request and recommends the small or large route. Holds `workflow-gates.md`, the rules for what each stage needs before it may start. |
| `feature-refine` | The detailed product interview for a large feature, one question at a time. |
| `feature-investigate` | Read-only look at how the repository behaves today, written up as private findings. |
| `feature-plan` | The implementation plan and test plan, from the spec and findings. |
| `feature-wireframe` | Designs the screens for a feature idea and publishes them as a private review page before anything is built. Inside a repository it reads the app's theme, components and the pages the idea touches, and draws the screens in the app's own design (low-fidelity wireframes on request). One panel per screen in flow order, states as tabs, Before/Now for changed screens, numbered notes, and two side-by-side options wherever there is a real design choice. Works on its own or inside a `/feature` job. `example/` holds a low-fidelity demo on a made-up billing app. |
| `review-walkthrough` | Builds a one-page cue sheet for an in-person review of a branch or PR. Changes are sorted into four zoom levels (System, Module, Function, Line); Quick shows only the highest level with changes, with Explain jumps to a short before/now explanation, and a view picker shows all levels or any one. A wrap-up collects follow-ups. |

### Agents (`agents/`)

Each file sets a worker's model, effort and tools. The Foreman dispatches them; you never call them directly.

- **Writers:** `feature-spec-writer`, `feature-wireframer` (draws the spec's screens with the `feature-wireframe` skill), `feature-investigator`, `feature-planner`, `feature-implementer`, `feature-tester`.
- **Review lenses**, run in parallel on the finished code: `feature-reviewer` (spec conformance), and `feature-review-permissions`, `-db`, `-tests`, `-ui`, `-errors`, `-performance`, `-conventions`.
- **`feature-fable-check`:** a short, independent second look at one document or change, on request.

## Screens before building

Run `/feature-wireframe <idea>` (or pass a spec path) inside the repository the feature belongs to. You get a link to a private page:

- **Screens in the app's own design.** It copies the app's Tailwind theme and component styles, so a new button or dialog looks the way it will when built. **Screens: Light/Dark** shows both themes; **100%** shows a screen at actual size. Add "low-fi" for greyscale wireframes instead.
- **Pink dashed outlines** mark what the feature adds; numbered pins match the notes under each screen.
- **Design choices** show two options side by side, one marked Recommended. Pick one with **Pick A / Pick B** (or the `A` / `B` keys).
- **Verdicts and notes** per screen save with the page. Tell Claude you've reviewed it and it reads them from the page, or use **Copy feedback** and paste. It revises the same page.
- **Questions to settle** lists open decisions and the assumptions it made.

Inside a `/feature` job the same skill runs as the **Screens** stage: the `feature-wireframer` worker draws the screens from the agreed spec and writes `wireframes.html` (opens straight from disk; the Feature Workshop shows it in its Screens tab, where verdicts and notes save in the browser) and `wireframes.json` (screens, choices, questions, version) to the job's folder. Nothing is published; your picks and notes come back as lines in your reply to the gate card. It only reads the repository (no servers, builds or tests) and invents all example data. Standalone pages are saved under `~/.claude/wireframes/<repo>/`.

## How a job runs

1. **Clarify.** For a standard or large job, the Foreman first asks up to five questions that would change what gets built, each with options, a recommendation and what each option means. Often there are none, and it goes straight to the spec.
2. **Spec.** The Foreman drafts a spec from your request and answers, and asks at most three questions.
3. **Route.** Each job gets a level of process, from a gate-free tweak to a full panel review. The Foreman suggests one from the request and the code it touches; you confirm or change it. Risky changes (migrations, auth, scoping, email) always get more review.
4. **Screens.** When the spec names a page, dialog, sheet or email, the screens are drawn for review before any code; what you pick goes into the spec. Skipped when there is nothing to draw.
5. **Investigate and plan.** Read-only findings, then a plan you approve before any code is written (a tweak at L0 builds straight from your request).
6. **Build.** A fresh implementer per plan step, one local commit per step, in its own git worktree.
7. **Test and review.** The test plan runs; review lenses report; fixes get one round by default.
8. **PRs.** Pushed to your fork only. Pull requests to the organisation repository are opened only when you say so.

Every job keeps its own private folder under `~/.claude/feature-work/<slug>/` with the spec, findings, plan, briefs and a `status.json` the dashboard reads. Nothing from that folder is committed to the repository you are working on.

## Adapting it

- `skills/feature/git-workflow.md` and `skills/feature-spec/workflow-gates.md` describe one team's remotes, branch naming and PR stages. Edit them for yours.
- `skills/feature/checklists/` holds the review checklists per area (API, database, email, UI). Add your own.
- Model choices live in each agent's front matter; a job's options can set the build and test models per job.

## Credits and license

Planned changes for test-first building, checking before claiming done, and systematic debugging draw on ideas from [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT). They are rewritten in this workflow's own words.

MIT licensed. See [LICENSE](LICENSE).
