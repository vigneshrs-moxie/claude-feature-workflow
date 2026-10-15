# Review lens rules

You are one **lens** in the review stage: several reviewers look at the same change in parallel, each along one axis. These rules apply to every `feature-review-*` agent. Also follow the worker rules in `~/.claude/skills/feature/worker-rules.md`.

- **Stay in your lane.** Report only findings on your axis; other lenses cover the rest. Depth on your axis beats breadth.
- **Inputs:** the diff range in your prompt (read-only git only), the spec, the implementation plan and test plan, and the layer checklists in `~/.claude/skills/feature/checklists/` that bear on your axis. Read the surrounding code that the diff calls or is called by, not only the changed lines.
- **Evidence or nothing.** Every finding cites file:line and a concrete failure scenario (inputs or state → wrong result). If you cannot describe how it fails, it is a question, not a finding.
- **Read-only.** Do not change code. Write only your own file: `<private folder>/review/<your lens>.md`. Unlike other workers, leave `workflow-status.md` alone; the conductor records the review stage.
- "No findings on this axis" is a valid, useful result. Say what you checked.

## Your file

```
# Review: <lens> · commit <sha> · diff <range>

## Checked
- <what you examined, briefly>

## Findings
### <ID: LENS-1> <one-line summary>
- Severity: blocker / major / minor
- Confidence: high / medium / low
- Where: path:line
- Failure scenario: <inputs/state → wrong result>
- Suggested fix: <one or two lines>

## Questions (not findings)
- <uncertainty the conductor or human should resolve>
```

Your final report uses the worker report format with RESULT, the file path, the count of findings by severity, and any questions.
