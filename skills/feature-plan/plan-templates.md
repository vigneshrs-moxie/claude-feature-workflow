# Plan templates

Private engineering artifacts. Size each section to the change; a small enhancement may need a line per section. Write "None." or "Not applicable" rather than deleting a section.

## implementation-plan.md

```markdown
# <Feature name>: implementation plan

| | |
|---|---|
| **Plan version** | 1 |
| **Date** | YYYY-MM-DD |
| **Basis** | spec <path> v<x.y> (<status>) · findings v<n> · commit <sha> |
| **Planning authorization** | <full / provisional: scope>, per workflow-status.md |
| **Approval** | Not approved |

## Proposed solution
<A short description of the approach.>

## Alternatives considered
| Option | Why not chosen / when it would win |
|---|---|

## Requirement traceability
| FR | Plan steps | Status |
|---|---|---|
| FR-001 | S1, S3 | Ready / Conditional on Q<n> / BLOCKED on Q<n> |

## Steps
### S1: <name>
- Layers: <db / api / ui / email>
- Files / areas: <paths from findings>
- Change: <what changes>
- Depends on: <step or decision>

## Data and migrations
<new or changed data, migration order and numbering per findings, backfill, rollback>

## Permissions
<who can do what, including direct-request checks>

## Notifications and email
<what is sent, when, to whom; how tests are kept from real recipients>

## Failure cases
| Situation | Handling | Covers |
|---|---|---|

## Branch, PR and release
<base branch and PR target per findings; conflicts awaiting decision; migration/deploy order>

## Risks and open questions
- <risk or Q-id> — <impact> — <who decides>
```

## test-plan.md

```markdown
# <Feature name>: test plan

| | |
|---|---|
| **Test plan version** | 1 |
| **Date** | YYYY-MM-DD |
| **Basis** | spec v<x.y> · findings v<n> · implementation plan v<n> · commit <sha> |
| **Approval** | Not approved |

## Acceptance traceability
| AC | Test(s) | Level (unit / integration / DB / manual) | Status |
|---|---|---|---|
| AC-001 | T1 | | Ready / Conditional / BLOCKED on Q<n> |

## Tests
### T1: <name>
- Covers: AC-00x
- Setup / data: <representative data>
- Steps and expected result:

## Permission and leakage tests
<non-authorized roles, direct requests, data that must not appear for other users>

## Test environment and data
<environment with the correct schema; representative records; how email is captured or redirected so no real recipient is reached>

## Validation commands (proposed, not run)
| Command | Source (script/doc) | Writes data? |
|---|---|---|

## Independent review
<who or what reviews the implementation separately, and against which artifact versions>

## Not covered
- <gap and why>
```

## acceptance.md

What the feature needs before it is **ready for staging**: what we accept as OK to push to staging and show stakeholders. Written in plain words a stakeholder would recognise in a demo, not in test terms. Approved by version with the plan. It goes to the reviewer (Raj) in the PR #2 body.

```markdown
# <Feature name>: acceptance criteria (ready for staging)

| | |
|---|---|
| **Version** | 1 |
| **Basis** | spec v<x.y> (or quick plan v<n>) · implementation plan v<n> |
| **Approval** | Not approved |

## The feature does
1. **A-1** <An outcome someone can see in a demo: who, where, what happens. "A manager can add a note to any customer in their office and sees it at the top of the Notes tab.">
2. **A-2** <…>  (3–7 items; each maps to one or more spec ACs: "covers AC-001, AC-002")

## It must not
- **A-N1** <What must stay as it is, or must not be possible: "A tech can't see notes." "The customer list loads as before.">

## Before it goes to staging
- [ ] `cd app && npm run check` and `cd app && npm run build` pass on the branch
- [ ] Every dev test in `dev-tests.md` passes, or its failure is named and accepted
- [ ] No errors in the browser console on the pages touched
- [ ] Database changes: <none | migration `NNNN_name`, applied to staging <before | after> merge>
- [ ] <Anything else this job needs: copy reviewed, flag on, …>

## Status
| Item | Met? | How we know (dev test, check, review) |
|---|---|---|
| A-1 | Not yet | |
```

## dev-tests.md

Simple ways for the developer to test what was built, by hand, on the job's branch (the Feature Workshop's Try it tab or a local server). **One line each**: who, where, what you do, what you should see. The developer runs these before PR #1; the same list goes to the reviewer in the PR #2 body.

```markdown
# <Feature name>: dev tests

| | |
|---|---|
| **Version** | 1 |
| **Basis** | acceptance v<n> · implementation plan v<n> |
| **Setup** | <branch, database changes to apply, test user(s) and role(s), data needed> |

| # | Test (as who → where → do → see) | Covers | Result |
|---|---|---|---|
| D-1 | Office manager → Customers → any customer → Notes → add "hello" → it shows at the top with your name and today's date | A-1 | |
| D-2 | Tech → same customer → the Notes tab isn't there | A-N1 | |

5–10 lines: the main path, an empty state, a permission or role case, one edge case (long text, zero rows, a bad input), and each "It must not" item. Result: `pass`, `fail: <what happened>` or `not run: <why>`.
