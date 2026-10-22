# PR body skeletons

The organisation's PR template (`.github/PULL_REQUEST_TEMPLATE.md` in the git workflow docs) is the source; these are its sections filled the way the team writes them: short, concrete, nothing claimed that didn't run. Keep the section headings, drop the checkbox lines you don't need, and end every body with the attribution line your session carries for pull requests.

## PR #1 (fork → same-named org branch)

```markdown
## Purpose and ticket

<One paragraph: what the change lets someone do, and why. Ticket or spec link, or "no ticket; requested by …".>

## PR stage

- [x] **#1 Fork intake:** `<fork owner>/<fork repo>:<branch>` -> `<org>:<branch>` (developer self-review + manual merge)

**Head:** `<fork owner>/<fork repo>:<branch>` @ `<sha>`
**Base:** `<org>:<branch>` @ `<sha>` (created from `main` @ `<sha>`)
**Earlier-stage PRs:** <none, or what this builds on>

## Changes

- <What changed, grouped by area; the user-visible behaviour first, then how.>
- <Non-obvious choices, in one line each.>
- Screenshots: <attached | not captured; checked on a local server on <date>>

## Test evidence

- `cd app && npm run check`: <exit 0: typecheck clean, lint N errors, Vitest N files / N tests | not run>
- `cd app && npm run build`: <exit 0 | not run>
- Focused tests: <files, counts>
- Manual: <what was tried, where, by whom>
- Not run: <what and why>. Full CI does not run on PR #1.

## Risk, rollout, rollback

- Database: <none | migration `NNNN_name`: what it creates; pre- or post-deploy; number checked against main (highest NNNN) and staging (highest NNNN)>
- Auth, roles, office scope: <none | what changed and how it was checked>
- Email, integrations, config, dependencies: <none | …>
- Rollback: <revert the merge commit | plus what a reverted migration leaves behind>

## Review

Self-review of the full diff: <what you checked, what you changed or accepted>. AI review: <not used | findings and their disposition>. I merge this myself once satisfied; Raj's review comes at PR #2.
```

## PR #2 (org branch → staging)

```markdown
## Purpose and ticket

<Same paragraph as PR #1, updated.>

## PR stage

- [x] **#2 Staging:** `<org>:<branch>` -> `<org>:staging` (Raj's review required)

**Head:** `<org>:<branch>` @ `<sha>`
**Base:** `<org>:staging` @ `<sha>`
**Earlier-stage PRs:** PR #1 = #<n> (fork -> org branch), merged <date>.

**Scope check:** `git log moxie/staging..moxie/<branch>` lists only this task's <n> commits, plus the PR #1 merge and <n> merges of main into the branch. Diff against staging: <n> files (+a / −b), the same set as against main. <Or: what else is in it and why.>

<If it conflicts with staging: the draft notice, the conflicting files and who changed them on staging, and that checks re-run after the sync.>

## Changes

<As PR #1, trimmed to what a reviewer needs.>

## Test evidence

<PR #1's evidence, plus: CI on this PR (link), and anything re-run against staging.>

## Risk, rollout, rollback

<As PR #1; migration numbers re-checked against the current staging; what to apply to the staging database before or after merge, if anything.>

## Review and approval

Raj: please review and submit an approving review on the latest commit. <Domain reviewers if any.> A human merges after approval and green checks.
```

## PR #3 (staging → main, the release summary)

```markdown
<One paragraph: what goes to production, for whom, and what customers notice.>

## Included

- #<n> <title> (<branch>, <author>, merged <date>): <one line on the change>
- …every PR merged into staging since main, not only the one that prompted this release…

## Database and configuration

- Migrations in this release: <`NNNN_name` … | none>. Order: <apply before deploy: … | after deploy (the automatic job): …>.
- Config, secrets, flags, dependencies: <none | …>

## Evidence

- Staging deployment: <sha / link>, tested by <who> on <date>: <what passed>; known issues: <…>
- CI and security on staging head: <link, result>
- Migration numbers checked against main: <ok | …>

## Release

- Release owner: <name>. Production trigger: <as configured; the owner confirms before merging>.
- Rollback: revert the merge commit; <what migrations leave behind>.
- After deploy: <smoke tests to run, by whom>.

Approval from someone other than the author is required before a human merges.
```

## Sync PR (fork → org branch, after resolving conflicts with staging)

```markdown
Merge-conflict fix for PR #2 #<n>; no new feature work.

The diff is large because it carries every staging change this branch had not seen (<n> files). All of it is already on staging and reviewed there; PR #2 goes back to only this task's files once this merges.

## Hand-written changes

- `<file>`: <what conflicted and how it was resolved>
- …

Review the merge commit `<sha>` rather than the whole diff.

## Checks

<focused tests, `npm run check`, and the scope check `git diff --stat moxie/staging HEAD` listing only this task's files>

Rollback: revert the merge commit on the org branch.
```
