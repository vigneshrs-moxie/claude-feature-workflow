---
name: review-walkthrough
description: Build an in-person review walkthrough page for the current branch or a PR and publish it as a private artifact. It sorts every change into five levels (Product, Rules, Structure, Code, Detail) and has a Quick/Full switch. Quick shows only what people see and how it behaves, in plain English, for a product demo. Full adds architecture, code and fine print as tickable cues. Each section has a verdict and notes, plus a file list, a timer and a wrap-up that collects follow-ups. Use when the user asks for a review walkthrough, a review doc, a code review support page, or "prep this for review".
---

# Review walkthrough

A one-page **cue sheet** for an in-person review. The user talks; the page gives them something to talk from and somewhere to record the outcome.

Most reviews are **product reviews**: the user shows a reviewer (often Raj, ~30 minutes, 2–3 PRs) what changed in the product, and the reviewer suggests behaviour or workflow changes. No code is shown. So the page opens in **Quick** mode, which is plain English about the product only. **Full** mode adds the engineering levels for a code review. One button (or `M`) switches.

`template.html` holds all styling and behavior and `build.py` fills it from git. You write only the `<section>` blocks. The page already provides:
- **Header:** title, branch, SHA and PR; **Quick / Full** switch; **Diff** button; **Files** dropdown with +/− counts and GitHub links; review **timer**; **A+** for a TV; **Copy follow-ups**.
- **Section strip** with a status dot per section and an "x/y reviewed" count for the sections in the current mode.
- **Pointers:** each bullet in `ul.points` gets a tick box.
- **Per section:** verdict buttons (Looks good / Question / Needs change) and a notes box.
- **Wrap-up:** a tally, every question, change request and note (from both modes), and a legend of the five levels.
- **Keys:** `M` Quick/Full, `J`/`K` next/previous section, `1` `2` `3` verdict, `N` notes, `Esc` leave notes, `T` timer.

Verdicts, ticks and notes save to the artifact's database by section key, so republishing keeps them.

Be fast. Don't ask questions unless the base branch can't be worked out. Don't run tests, typechecks or linters. Report only what this session, the PR or the history shows, and say plainly what hasn't been run.

## The five levels

Every change in the diff belongs to exactly one level. Sort by the first question that answers yes.

| # | Name | Test | Shown in |
|---|---|---|---|
| 1 | **Product** | Would someone using the product notice it? A new button, page, column, flow, wording, or email they receive. | Quick + Full |
| 2 | **Rules** | Does it change what happens without a visible control? Who is allowed, when an email goes out, what is blocked, what is kept, copied or cleared, what happens on failure or a double click. | Quick + Full |
| 3 | **Structure** | Would an architect draw it on a whiteboard? A new table or migration, a new endpoint or server action, a new module, logic moved between frontend and backend, a new shared piece. | Full |
| 4 | **Code** | Would a reviewer read it in the diff? Which functions and components implement it, and the tests. | Full |
| 5 | **Detail** | Does it only matter to someone reading the line? Race guards, edge cases, browser quirks, isolation levels, cleanups, comments. | Full |

One real change often shows up on several levels: "bulk close" is a bar (1), never overwrites a reply (2), a new endpoint (3), `applyBulk` and `BulkBar` (4), and a reply-aware update guard (5). Write each level's part at its own level. Never let a lower level leak upward: no file, function, table or endpoint names in Levels 1–2.

## 1. Gather the facts (in parallel)

- **Base:** `moxie/main` in moxie-portal, otherwise `upstream/main` or `origin/main`. Use the merge-base. Don't fetch without asking. A PR into `staging` still diffs against main's merge-base, because staging diverges.
- **For a PR link:** `gh pr view <n> --repo OWNER/REPO --json title,body,headRefName,headRefOid,baseRefName,commits` and `gh pr checks`. If the head isn't local, find a worktree or remote branch with the feature (`git worktree list`, `git branch -r`), and confirm with `gh api repos/OWNER/REPO/compare/<local>...<head>` that the remaining commits change no files.
- `git log --oneline <mb>..HEAD`, `git diff --stat <mb>..HEAD`, then read `git diff <mb>..HEAD` file by file. Skip lockfiles and generated files. Save large diffs to the scratchpad and read them.
- The PR body and this conversation: why it was made, decisions, known limits, check results.
- Note **real problems** for "Fix before merge": stale comments, leftover debug code, removed lint suppressions, risky migrations, missing null handling, migration-order traps.

## 2. Build the level map (before writing anything)

Write `<scratchpad>/levels.md`: for each of the five levels, list every change at that level in one line each. Read the diff for this, not just the PR body; the PR body tells you what was meant, the diff tells you what happened. Then check:
- Every user-visible change in the diff has a Level 1 line.
- Every Level 3 item (each new table, endpoint, module) has at least one Level 1 or 2 line explaining why a person would care. If it has none, it's an internal refactor: say so in the footprint line.

## 3. Write the sections

Write them to `<scratchpad>/sections.html` in this order. Drop any that would be empty, except `product`.

| key | attrs | step label | h2 | contents |
|---|---|---|---|---|
| `product` | `data-quick data-level="1"` | Level 1 · Product | What people see | `<p class="lede">` why, one sentence. `<p class="footprint">` "Under the hood: …", one sentence sizing Level 3 in plain words. Then `ul.points`, 3–6 items. |
| `try` | `data-quick` | Show it | Demo | `.try` with 3–5 steps: page, role, click, what you see. Only if something is user-facing. |
| `rules` | `data-quick data-level="2"` | Level 2 · Rules | How it behaves | `ul.points`, 2–6 items. |
| `decide` | `data-quick` | For discussion | Questions to settle | `ul.points`, each starting `<span class="flag">Decide</span>`. Product and workflow questions a reviewer can answer without code, plus deployment steps someone must own. |
| `structure` | `data-level="3"` | Level 3 · Structure | How it's built | `<h3>` per layer that changed (Frontend / Backend / Data / Shared), 1–3 pointers each. Optional `.compare` Before/Now when the shape changed. |
| `code` | `data-level="4"` | Level 4 · Code | Code changes | `<h3>` per mechanism, 1–4 pointers with file chips. A `<pre>` of 1–3 lines only when a signature says it faster. |
| `detail` | `data-level="5"` | Level 5 · Detail | Fine print | `ul.points` of guards, edge cases and quirks, with file chips. Then one pointer summarising the tests. |
| `ship` | | Ship it | Ship it | Migration (+ rollback), risk, "Fix before merge" with `<span class="flag">Fix</span>` (or "nothing found"), Checks, Review, Next. |

### Writing Levels 1–2 and Decide (Quick mode)

These are read aloud to someone who won't see code.
- **Plain English, full sentences.** One or two sentences per item, about 15–35 words. A person who has never seen the codebase understands it.
- **Start with who or what the person sees:** "Admins can…", "The Feedback list now…", "A ticket moved back to In progress…".
- **Use the product's names** for pages, buttons and statuses, in their exact on-screen wording. Bold the first few words naming the thing.
- **No code words:** no file, function, table, endpoint, transaction or migration names, no "API", "server action", "state". Say "saved", "all or nothing", "only admins", "the page reloads".
- **Say the effect, not the mechanism:** "a double click makes one copy, not two", not "buttons disabled while busy".
- **At most six items per level.** Merge or drop the rest; the rest belongs lower.
- **Footprint line:** one sentence, counts in words: "Under the hood: one new database table and two new server endpoints; no permission changes."

### Writing Levels 3–5 (Full mode)

These are cues for a code review.
- **Each pointer is a cue, not an explanation.** About 4–12 words, fragments are fine, nouns first. Example: `<strong>Submit</strong> disabled until every 1 has a comment`.
- One idea per pointer. No "because" clauses; the user says those out loud.
- Bold the first word or two when it names the thing.
- Put a file chip inline at the end of the pointer it supports.

### Section shape

`data-key` is stable; keep the same keys on republish.

```html
  <section data-key="product" data-quick data-level="1">
    <div class="content">
      <p class="step">Level 1 · Product</p>
      <h2>What people see</h2>
      <p class="lede">Admins can start a Role Template from an existing one instead of from blank.</p>
      <p class="footprint">Under the hood: one new server action and a copy routine; no database changes.</p>
      <ul class="points">
        <li><strong>"Copy from Template"</strong> is a new button on the Role Templates page. It opens a searchable list of every template, and picking one creates the copy and opens it.</li>
      </ul>
    </div>
    <aside><textarea id="n-product" aria-label="Notes" placeholder="Notes"></textarea></aside>
  </section>

  <section data-key="code" data-level="4">
    <div class="content">
      <p class="step">Level 4 · Code</p>
      <h2>Code changes</h2>
      <h3>Server action</h3>
      <ul class="points">
        <li><strong>copyRoleTemplate(sourceId)</strong>: admin check, then copy <span class="files"><a href="{{BLOB}}/app/src/lib/actions/admin.ts#L135" data-file="app/src/lib/actions/admin.ts" data-line="135"><code>admin.ts</code></a></span></li>
      </ul>
    </div>
    <aside><textarea id="n-code" aria-label="Notes" placeholder="Notes"></textarea></aside>
  </section>
```

Other blocks:

```html
<div class="try"><h4>Try it</h4><ol><li>…</li></ol></div>
<div class="compare"><div><h4>Before</h4><ul><li>…</li></ul></div><div><h4>Now</h4><ul><li>…</li></ul></div></div>
<details class="more"><summary>Show code</summary><pre><code>…</code></pre></details>
```

Quick mode hides file chips, `<pre>` and `details.more` automatically, so a stray chip in Level 1–2 won't show, but don't write one.

**File chips:** use `{{BLOB}}/path#L<n>` with `data-file` and `data-line`; `build.py` fills in the repository and head commit. Add `data-line` and `#L` only for lines confirmed with `grep -n` (on `git show <sha>:<path>` when the code isn't checked out). If the commit isn't pushed, use `<code data-file="…">` with no link. Escape `<`, `>` and `&` in code.

## 4. Build and publish

Run from the checkout or worktree that holds the feature:

```bash
cd <worktree> && python3 ~/.claude/skills/review-walkthrough/build.py --title "Short feature name" --sections <scratchpad>/sections.html [--pr <url>] [--mode full]
```

- `--pr` makes the header, Diff button and all links point at that PR's repository and head commit. Use it whenever reviewing a PR, especially from a fork checkout.
- `--mode` sets the mode the page first opens in. Default `quick`. Use `full` only when the user says the review is a code review.

The script writes `~/.claude/review-walkthroughs/<repo>/<branch>.html` and prints the existing artifact URL, if this branch has one.

- **Existing URL, published earlier in this conversation:** publish the same file path again. **From an earlier conversation:** read it (`action: "read"`) first, then publish with that `url`. Either way leave out `icon` and `capabilities`.
- **New:** load the `artifact-capabilities` skill. Publish with `icon: "review"`, a one-sentence `description` and `capabilities: {"db": {}, "user": {}}`. Then write the URL into the `.url` file the script named.
- Reply with the link and the "Fix before merge" items, one line each. Don't repeat the rest of the page.
