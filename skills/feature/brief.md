# Brief format and review checklist

## Review checklist (run before every brief)

Check the artifact **on disk**, not the worker's summary of it.

- **Traceable:** every V1 FR has an AC; every AC has a test in the test plan; every plan step cites FRs. For a quick plan or `requirements.md`: every numbered criterion has a check or a manual step.
- **Nothing invented:** no business rule, permission, audience, timing or notification behavior that the spec does not confirm. Recommendations stay labeled.
- **Evidence:** claims about the code cite file:line; spot-check two or three of the citations yourself.
- **Honest checks:** "ran" vs "proposed" is accurate; nothing claims a check passed that did not run.
- **In scope:** no scope creep beyond V1; nothing outside the allowed writes (application files only during implementation, on the feature branch).
- **Versions:** every artifact names the versions it is based on, and those match what is on disk.
- **Gates:** the worker stopped where it should and did not start the next stage.
- **Proportional:** a small enhancement did not get a large-feature treatment.
- **Options followed:** the level, stages, reviewers, checks and models match the job's `options.json` at the time.

## Brief format

Aim for about 12 lines; a brief asking to approve what will be built (a quick plan or a plan; at L0 usually none; the first brief shows the diff) may run to about 25, so the human can decide without opening a file. Plain language. No restating the artifact. Write the brief file and `status.json` with one Write each (never with scripts or several edits).

```
**<Feature> · <stage> done** · spec v<x> (<status>) · <other artifact> v<n>

**What happened**
- <3–5 bullets: the outcome, the biggest finding or change, anything surprising>

**Concerns** (from my review; omit if none)
- <issue> — <what I did about it or what it means>

**Decisions for you** (omit if none; max 3, recommendation first)
1. <question> — Recommended: <answer>. <one-line tradeoff>
2. …

**Next:** <proposed stage, one line on what it will and won't do>
Reply "go" to proceed<, or answer like "1a 2 yes">. Full details: <artifact paths>
```

When the human asks for detail on one point, answer that point from the artifact; do not paste the artifact.
