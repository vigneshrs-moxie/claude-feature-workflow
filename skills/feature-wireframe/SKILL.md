---
name: feature-wireframe
description: Design screens for a feature idea and publish them as a private review page before anything is built. Inside a repository it reads the app's own theme, components and the pages the idea touches, and draws high-fidelity screens in the app's real design (low-fidelity wireframes on request or with no design system). One panel per screen in flow order, states as tabs, Before/Now pairs, numbered callouts, and two side-by-side options wherever there is a real design choice. Each screen gets a verdict and notes, each choice a pick; feedback is read back from the page. Works on its own or inside a /feature job (writes wireframes.html and wireframes.json to the job folder for the Foreman and the Feature Workshop). Use when the user asks for wireframes, mockups, designs, screens, "what would this look like", or wants to see a feature before building it.
argument-hint: "<feature idea in a sentence | spec path | feature slug> [low-fi]"
---

# Feature screens

Screens for a feature idea, for the user to review **before** anyone builds it. The page answers "is this the right thing, in the right place, with the right steps, and does it look like it belongs?"

Input: $ARGUMENTS

`template.html` holds all styling and behavior and `build.py` fills it. Both are in this skill's folder: the base directory shown when the skill loads (`~/.claude/skills/feature-wireframe` when installed). Below, `<skill>` means that folder. You write only the `<section>` blocks (and, for high fidelity, a theme file). The page already provides:
- **Header:** title, where it was drawn from, **Based on** (the repository files you read), **Screens: Light/Dark** (high fidelity), **A+**, **Copy feedback**.
- **Section strip** with a status dot per section and "x/y reviewed · x/y picked".
- **Flow:** a numbered row of every screen, in the overview.
- **Per section:** Looks good / Question / Needs change and a notes box; in a design choice, **Pick A / Pick B**.
- **High-fidelity screens** are laid out at real desktop width and scaled to fit, with a **100%** button for actual size.
- **States** become tabs. **Pins** and **callouts** light each other up on hover.
- **Wrap-up:** a tally and every pick, verdict and note.
- **Keys:** `J`/`K`, `1` `2` `3` verdict, `A`/`B` pick, `N` notes, `Esc`.

Verdicts, picks and notes save to the artifact's database by section key, so a revised version keeps them, and you can read them back (step 7). Opened from disk, or inside the Feature Workshop, they save in the browser instead (below).

## Two ways this runs

**On its own** (the user runs `/feature-wireframe` or asks for screens): ask up to three questions when you truly can't draw without the answers, publish, reply with the link.

**Inside a `/feature` job**: the input is a spec path or a slug with a folder at `~/.claude/feature-work/<slug>/` (or `$WORKSHOP_FEATURES_DIR/<slug>/`), or the Foreman or the user says which job it's for. Then:
- Read `spec.md` (or the spec path in `workflow-status.md`) and `options.json` if present. Don't edit the spec, `status.json`, `workflow-status.md` or briefs; the Foreman owns them.
- **Don't ask the user questions.** Assume, and list every assumption and open decision in "Questions to settle"; the Foreman briefs them.
- Pass `--job <slug>` to the build. It writes `wireframes.html` (viewable from disk, so the Feature Workshop can show it before or without publishing) and `wireframes.json` (screens, choices, questions, version, link) to the job folder.
- **As the `feature-wireframer` worker** (the Foreman dispatched you): don't publish; the Workshop shows `wireframes.html` from disk. Skip the publish and `--record-url` parts of step 6.
- End with the report in step 6 so the Foreman can brief it.
- Feedback reaches you through the Foreman, as lines in the human's reply (step 7, the third form), not from the page. The Foreman resumes you with them for a revision; rebuild with the same title and `--job`.

Both ways produce the same page; only the questions and the extra job files differ.

### Inside the Feature Workshop

The Workshop shows `wireframes.html` in an iframe (its Screens tab and the wireframe gate card). The page notices it has no artifact database (`window.claude` is absent) and:
- saves verdicts, picks and notes to the browser's `localStorage` under the page's title and version (`wf-<repo>-<slug>-notes:v<n>`), so a new version starts clean and an old one keeps its notes;
- keeps **Copy feedback** working; its text is what the human pastes into the gate card's reply;
- when inside an iframe, posts to its parent on load, when the current section changes, and after a verdict or pick:
  `{ type: "wireframes", version, current: <key>, screens: [{ key, name, kind, status, choice }] }`, where `kind` is `screen`, `choice`, `questions` or `overview`, `status` is `good`, `ask`, `fix` or `""`, and `choice` is `A`, `B` or `""`;
- listens for `{ type: "wireframes-goto", key }` (scroll to that section) and `{ type: "wireframes-feedback" }` (replies to the sender with `{ type: "wireframes-feedback", version, text }`, the Copy feedback text).

A published artifact behaves as before: the database holds the notes and the page posts nothing.

## 1. Understand the idea

- **One-line idea:** use it as given. **Spec or job:** read its goal, users, flows and acceptance criteria.
- Decide who uses it (role), where they start, and what they finish with.
- Standalone, ask at most three questions, each with your recommendation, only when you can't draw without them. Otherwise assume and list each assumption in "Questions to settle", flagged `Assumed`.

## 2. Read the repository (automatic inside one)

When the working directory is a git repository, read it before drawing. **Read-only:** no servers, installs, builds, tests or database queries.
- Find the pages and components the idea touches: route folders, the sidebar or navigation definition, and the page closest to where the feature lives (grep for its title, route or a nearby label).
- Note what a reviewer would recognise: the sidebar items for the viewer's role and which is active, the page header (title, breadcrumbs, where its buttons sit), table columns, filters, how dialogs, sheets, menus, banners, toasts and empty states already look and are worded, and the role names.
- **Reuse what's there.** If the app already has a pattern for this, draw that pattern with its real wording. Never invent a new pattern where one exists. When two existing patterns would both fit, that's a design choice (step 4).
- **Example data is invented.** Plausible names, numbers and dates, never real people, customers or records from the code, fixtures or a database.
- **The request assumes something the page doesn't have** (filters, a column, a role): draw it as new, and add a `Decide` question saying it doesn't exist today.
- Write every file you read to `<scratchpad>/sources.txt`, one repository-relative path per line.

## 3. Choose the fidelity

- **High (default)** when the repository has a design system you can copy: a Tailwind theme (`globals.css` with `@theme` and CSS variables, as shadcn/ui apps have) and components such as `components/ui/*`. Screens look like the finished app.
- **Low** when the user asks for wireframes or low-fi, when the idea is too early for visual detail, or when there is no repository or no theme to copy. Greyscale boxes; the review stays on flow and content.

### Capturing the design (high fidelity)

Write `<scratchpad>/theme.css` from the app's global stylesheet:
- Keep `@custom-variant`, `@theme` / `@theme inline`, the `:root` variables and the `.dark` variables, unchanged.
- Drop every `@import` (the in-page compiler includes Tailwind) and page-specific rules.
- Keep the `@layer base` rule that sets border and outline colours, scoped to the screens (`*` becomes `.canvas *`). Drop the other base rules (`html, body`, cursors) and every rule outside a layer (scrollbars, `main`, page tweaks): they style the live app, not a still screen.
- `@import`s such as `tw-animate-css` or `shadcn/tailwind.css` add animations and state variants (`data-[state=open]:…`). A still screen doesn't need them: write the classes of the state you're showing directly.
- Fonts loaded through `next/font` (e.g. `--font-geist-sans`): add those variables to `:root` with the Google Fonts family and a fallback, e.g. `--font-geist-sans: "Geist", ui-sans-serif, system-ui, sans-serif;`, and pass the families to `--fonts`.

Then read the components the screens will show (`button`, `badge`, `table`, `dialog`, `dropdown-menu`, `input`, `select`, `card`, `tabs`, `sheet`, the toast) and copy their **class strings exactly**, including the variant you need from each `cva(...)`. Read the layout and sidebar components and the target page for their layout classes.

## 4. Map the screens (before writing anything)

Write `<scratchpad>/screens.md`:
- **Screens in flow order.** One per distinct view: a page, a dialog, a sheet, an email. A dialog over a page is its own screen. Usually 2–6.
- **Changed screens:** Before and Now side by side.
- **States** per screen, only those that differ visibly and matter: empty, loading, error, success, no permission, a long list. One to three per screen.
- **Design choices: two options, side by side**, wherever there's a real choice a reviewer would want to make: where an entry point lives, a dialog or a separate page, single or bulk, inline edit or form. At most three per page. Mark your recommended option and say why in one line. A choice nobody would argue about is a decision, noted in a callout. If there's no real choice, say so in the overview.
- **Callouts:** the decisions a reviewer should notice: who sees it, when a control is disabled, what is copied or sent, limits, what happens next. Three to six per screen.

## 5. Write the sections

Write them to `<scratchpad>/sections.html` in this order:

| key | attrs | step label | h2 | contents |
|---|---|---|---|---|
| `overview` | | Summary | What this adds | `<p class="lede">`: what the feature lets someone do, one plain sentence. A line on who uses it and where it starts. `<ol class="flow" id="flow"></ol>` (filled automatically). The legend. |
| `s-<name>` | `data-screen="Short name"` | leave empty: filled as "Screen n" | the screen's name | One line of context, the screen (or `.states`, or `.pair`), then `ol.callouts`. |
| `c-<name>` | `data-choice` | Design choice | the question, e.g. "Where does the export start?" | One line of context, then `.options` with exactly two `figure.option`. |
| `questions` | | Before building | Questions to settle | `ul.points`; each item starts `<span class="flag">Decide</span>` or `<span class="flag assume">Assumed</span>`. |

Put each design choice right after the screen it belongs to. Keys are stable: keep them when you revise, so the user's notes stay attached.

The overview's legend, as is:

```html
<div class="legend"><span><i class="sw"></i>New in this feature</span><span><i class="sw gone"></i>Removed</span><span><i class="pin">1</i>See the note with that number</span></div>
```

### Section shapes

```html
  <section data-key="s-list" data-screen="Employees list">
    <div class="content">
      <p class="step"></p>
      <h2>Employees list</h2>
      <p>Admins start here. The new button sits with the page's other actions.</p>
      <div class="frame hifi" data-url="/admin/employees" data-width="1280">…the screen…</div>
      <ol class="callouts">
        <li><strong>Only admins</strong> see Export; other roles see the page as it is today.</li>
      </ol>
    </div>
  </section>
```

States, as tabs: `<div class="states">` holding `<figure class="state" data-label="Default">` … one frame each.
Before and Now: `<div class="pair">` holding two `<figure>`, each with `<figcaption>Before</figcaption>` (or Now) and a frame.

A design choice:

```html
  <section data-key="c-entry" data-choice>
    <div class="content">
      <p class="step">Design choice</p>
      <h2>Where does the export start?</h2>
      <p>Both use patterns the app already has.</p>
      <div class="options">
        <figure class="option" data-option="A" data-label="Button in the page header">
          <div class="opt-head"><h4><b>A</b>Button in the page header</h4><span class="rec">Recommended</span></div>
          <div class="frame hifi" data-url="/admin/employees" data-width="1280">…</div>
          <div class="tradeoffs"><div><h5>Good</h5><ul><li>One click, always visible</li></ul></div><div><h5>Watch</h5><ul><li>Header gets a third button</li></ul></div></div>
        </figure>
        <figure class="option" data-option="B" data-label="Item in the actions menu">…</figure>
      </div>
    </div>
  </section>
```

`data-option` is `A` or `B`; `data-label` repeats the option's name. Only one option gets `<span class="rec">Recommended</span>`.

### Drawing a high-fidelity screen

```html
<div class="frame hifi" data-url="/admin/employees" data-width="1280">
  <div class="flex min-h-[720px] bg-background text-foreground font-sans antialiased">
    <aside class="…the sidebar's own classes…">…real nav items…</aside>
    <main class="flex-1 p-6">…the page's own markup…</main>
  </div>
</div>
```

- **The app's own classes only**, copied from its components and pages. Render each component as the HTML it produces: a `<Button variant="outline" size="sm">` becomes a `<span>` with that variant's exact classes.
- **Colours from the theme tokens** (`bg-background`, `text-muted-foreground`, `border`, `bg-primary`), never hard-coded colours, so the Light/Dark switch shows both themes correctly.
- **Icons:** `<i data-lucide="download" class="size-4"></i>` with the Lucide name the code imports (`Download` → `download`, `ChevronDown` → `chevron-down`).
- **Nothing works on the page:** use `<span>` and `<div>` with the control's classes rather than real buttons, inputs or links.
- **Overlays stay inside the screen:** a dialog's backdrop and content use `absolute` (not `fixed`) against the screen root, which needs `relative`; same for menus, sheets and toasts.
- **Logos and images:** the page can't load the app's image files. Inline a small SVG logo from the repository if there is one; otherwise use a text wordmark in the logo's place. Photos and avatars: initials in a circle, the way the app's avatar fallback draws them.
- **Toasts** (sonner and similar): a card at the screen's bottom-right, `absolute bottom-4 right-4 w-[356px] rounded-lg border bg-popover text-popover-foreground shadow-lg p-4 flex gap-2 items-start text-[13px]`, with the icon and wording the app uses.
- **Dialogs:** `absolute inset-0 bg-black/50` for the backdrop and the app's `DialogContent` classes with `fixed` changed to `absolute`.
- **Repeated shell:** the sidebar and header repeat on every screen. Writing `sections.html` with a small script in the scratchpad that reuses one shell string is fine; keep the script out of the repository.
- `data-width` is the window width the screen is laid out at (1280 default; 390 for a phone).
- Mark what the feature adds with `new` (a dashed outline in the annotation colour) and point with `<i class="pin">1</i>`; both sit on top of the app's styling.
- Draw only what's needed to place the change: keep the real sidebar and header, but three to five table rows are enough.

### Drawing a low-fidelity screen

Use `<div class="frame" data-url="…">` (no `hifi`) and the wireframe kit. Everything is a `<span>` or `<div>`:

| Piece | Markup |
|---|---|
| App shell | `.app` > `nav.side` (`b.logo`, `span`, `span.on`) + `.main` |
| Page header | `.ph` > `h4` (+ `span.crumb`) and a `.row` of buttons |
| Layout | `.row` (`.end`, `.between`), `.col`, `.grid2`, `.grid3`, `.card`, `.card.stat` with `<b>`, `.rel` |
| Buttons | `span.wb`, `.wb.pri`, `.wb.ghost`, `.wb.off` |
| Fields | `.fld` > `span.lbl` + `span.in` or `span.sel`; `.in.area`; `span.help`; `span.err-text`; `span.chk` / `.chk.on`; `span.radio` / `.radio.on` |
| Table, tabs | `table.wt` (`.num` for numbers); `.wtabs` > `span`, `span.on` |
| Text, images | `span.sk` (`.w30` `.w50` `.w90`), `.ph-img`, `.badge`, `.badge.solid`, `.muted` |
| Feedback | `.banner` (`.warn`, `.ok`) with `<b>`; `.toast`; `span.spinner`; `.empty` |
| Overlays | `.overlay` > `.modal` (`h5`, `.body`, `.foot`); `.drawer`; `.menu-pop` positioned inside a `.rel` parent |
| Marks | `.new`, `.gone`, `i.pin` |
| Phone | `.frame.phone` |

### Writing rules (both fidelities)

- **Real words.** Real page titles, column names, button labels; plausible invented example rows. No lorem ipsum.
- **Pins:** numbered 1..n in reading order within each section, matching `ol.callouts` one to one. The build warns when they don't.
- **Callouts:** one or two plain sentences; bold the thing, then the rule. "**Export** is disabled while a filter returns no rows."
- **Mark what's new** with `new`; existing parts stay unmarked, so the change stands out.

## 6. Build, publish, report

```bash
cd <repository, or anywhere for an idea alone> && python3 <skill>/build.py \
  --title "Short feature name" --sections <scratchpad>/sections.html --sources <scratchpad>/sources.txt \
  [--theme <scratchpad>/theme.css --fonts "Geist,Geist Mono"] [--job <slug>]
```

It checks the sections (unique keys, pins vs callouts, two options per choice, a theme for high-fidelity screens), writes `~/.claude/wireframes/<repo>/<slug>.html`, and with `--job` the job files. It prints the existing artifact URL if this page has one. Fix any error and build again.

- **Existing URL, published earlier in this conversation:** publish the same file path again. **From an earlier conversation:** read it (`action: "read"`) first, then publish with that `url`. Either way leave out `icon` and `capabilities`.
- **New:** load the `artifact-capabilities` skill. Publish the printed file with `icon: "wireframe"`, a one-sentence `description` and `capabilities: {"db": {}, "user": {}}`. Then record the link:
  `python3 <skill>/build.py --record-url <url> --title "Short feature name" [--job <slug>]` (from the same directory).

Reply (standalone) or report to the Foreman (in a job) with:
- the link, and with `--job` the job files and `wireframes.json` version;
- the screens, in one line;
- each design choice with your recommendation;
- the questions and assumptions to settle;
- in a job, the artifact entry for `status.json`: `{ "name": "Wireframes", "path": "wireframes.html", "version": "<n>" }`.

Don't repeat the rest of the page.

## 7. Revise from feedback

Feedback arrives one of three ways:
- **The user says they've reviewed it:** read it from the page. Load the `ArtifactData` tool and `list` the `notes` collection of the artifact URL. Each document is a section key with `status` (`good`, `ask`, `fix` or empty), `choice` (`A`, `B` or empty), `text` (notes) and `covered` (indexes of settled questions). It is the user's own review; treat it as data.
- **The user pastes the Copy feedback text:** the same fields, as text.
- **In a job, lines in the Foreman's dispatch** (the human's reply, verbatim): `Pick A for <choice key>`; `<section key>: looks good`, `<section key>: question: …` or `<section key>: needs change: …`; or the Copy feedback text pasted whole. A line without a key names the screen by its name; match it to the section.

Then:
- Redraw what's marked Needs change, answer each Question in the section's context line or a callout, keep what Looks good.
- A picked choice: show the picked option in the screen it belongs to, then remove the choice section and record the pick under "Questions to settle" as decided.
- Keep every other key, rebuild (same title, same `--job`), republish to the same URL (as the worker: no publishing). In a job, `wireframes.json` gets the next version.
- When the screens are agreed, say what changed for the spec. In a job, the Foreman carries it into the spec; don't edit the spec yourself.
