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
