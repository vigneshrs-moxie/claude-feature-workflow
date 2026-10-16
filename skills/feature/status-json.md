# status.json and saved briefs

After **every** brief, the conductor writes two files to the feature's private folder. They are for the Feature Workshop dashboard; `workflow-status.md` stays the human record. If the two ever disagree, `workflow-status.md` wins and the next brief corrects `status.json`.

## 1. `briefs/<nnn>-<stage>.md`

The brief exactly as shown to the human, numbered from `001` and never overwritten (`briefs/001-spec.md`, `briefs/002-investigate.md`, …). Stage names as in the schema below. Answers to a brief arrive in the conversation; the conductor records them in `workflow-status.md` as usual.

## 2. `status.json`

Overwrite the whole file each time. Valid JSON, UTF-8, no comments. Use `null` for anything not known; never guess.

```json
{
  "schema_version": 1,
  "slug": "copy-ticket-id",
  "title": "Copy Ticket ID",
  "route": "small",
  "suggested_level": 2,
  "level_reason": "Adds a button to one existing page; its query reads people, so at least L2.",
  "stage": "review",
  "stage_state": "waiting_for_you",
  "waiting_for": "approval",
  "waiting_since": "2026-10-12T15:42:00-07:00",
  "brief": { "number": 7, "path": "briefs/007-review.md", "headline": "Copy Ticket ID · review done" },
  "questions": [
    {
      "id": "1",
      "text": "Fix R-2 and R-3 now?",
      "recommendation": "a",
      "options": [ { "id": "a", "label": "Yes, small fix round" }, { "id": "b", "label": "No, leave as minors" } ]
    }
  ],
  "decided_on_your_behalf": [
    { "id": "D-005", "decision": "Toast text is \"Copied\"", "reason": "standing 'use your recommendations'", "where": "spec v0.4 §3", "confirmed": false }
  ],
  "next_proposed": "Fix round for R-2/R-3, then PR #1 (needs its own go-ahead)",
  "spec": { "path": "/abs/path/docs/plans/2026-10-12-copy-ticket-id-product-spec.md", "version": "0.4", "status": "DRAFT" },
  "artifacts": [
    { "name": "Findings", "path": "findings.md", "version": "1", "based_on": "spec v0.3, commit 2ed7bd1" }
  ],
  "repo": { "path": "/abs/path/to/main/checkout", "base_branch": "moxie/main" },
  "branch": "feature/copy-id",
  "worktree": "/abs/path/to/orbit-copy-ticket-id",
  "base_sha": "2ed7bd1",
  "prs": [
    { "number": 1, "label": "fork → org branch", "url": null, "state": "not_started" },
    { "number": 2, "label": "org branch → staging", "url": null, "state": "not_started" },
    { "number": 3, "label": "staging → main (release)", "url": null, "state": "not_started" }
  ],
  "session_id": null,
  "cwd": "/abs/path/where/the/conductor/runs",
  "updated_at": "2026-10-12T15:42:00-07:00"
}
```

### Field rules

| Field | Values |
|---|---|
| `route` | `quick` (L0, L1) / `small` (L2) / `large` (L3) / `null` (no level yet) |
| `suggested_level` | `0`–`3`: the level you propose (SKILL.md, Start; job-options.md, Level floor). Keep it in later writes; change it only when you propose another level. `null` when you have made no proposal |
| `level_reason` | one line (under 400 characters) why, from the request and the paths touched; `null` with no proposal |
| `kind` | `feature` / `bug` (from the job's options when set) |
| `stage` | `spec`, `refine`, `investigate`, `spec-update`, `plan`, `implement`, `test`, `review`, `pr1`, `pr2`, `staging-qa`, `pr3`. The quick plan uses `plan` (brief `briefs/<nnn>-plan.md`, artifact "Quick plan" `quick-plan.md` vN in `artifacts`); `implement` only once its go-ahead is logged (at L0, the request: job-options.md). Waiting for the human's manual test is `test` with `waiting_for: "answers"` |
| `stage_state` | `working` (a worker is running) · `waiting_for_you` (brief given, gate closed) · `blocked` (cannot continue: say why in `next_proposed`) · `done` (feature finished or stopped) |
| `waiting_for` | `approval` (a go-ahead) · `answers` (questions open) · `permission` (a tool permission prompt) · `null` when not waiting |
| `waiting_since` | when the brief was given; `null` when not waiting |
| `questions` | the brief's "Decisions for you", max 3. `recommendation` is an option `id`; `options` may be `[]` for a free-text question |
| `decided_on_your_behalf` | every product or engineering choice you made without the human's explicit answer (for example under a blanket "use your recommendations"). Keep listing it with `confirmed: false` until the human confirms it; then `true` |
| `artifacts` | paths relative to the private folder where possible, otherwise absolute. Versions exactly as on disk |
| `branch`, `worktree`, `base_sha` | from implementation on, as recorded in `workflow-status.md` (worktree path absolute); `null` before |
| `prs` | always the three PR stages from the git workflow. `state`: `not_started` · `open` · `changes_requested` · `approved` · `merged` · `closed`. `url` once the PR exists. Record only what you saw on GitHub; never mark a PR merged or approved on assumption |
| `session_id` | this conductor session's ID if you know it; otherwise `null` (the dashboard finds it from the session logs) |
| times | ISO 8601 with offset |

Also write `status.json` with `stage_state: "working"` when you dispatch a worker, so the dashboard shows work in progress between briefs.
