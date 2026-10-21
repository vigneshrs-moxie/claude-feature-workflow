---
name: feature-wireframe
description: Draw low-fidelity wireframes of a feature idea and publish them as a private review page before anything is built. One panel per screen in flow order, states as tabs, Before/Now pairs for changed screens, numbered callouts, and two side-by-side options wherever there is a real design choice. Inside a repository it first reads the existing pages the idea touches, so the wireframes use the app's real layout, labels and patterns. Each screen gets a verdict and notes, each choice a pick, and Copy feedback collects it all to paste back. Use when the user asks for wireframes, mockups, screen sketches, "what would this look like", or wants to see a feature before building it.
argument-hint: "<feature idea in a sentence | spec path | feature slug>"
---

# Feature wireframes

Low-fidelity screens for a feature idea, for the user to review **before** anyone builds it. The page answers "is this the right thing, in the right place, with the right steps?" It does not answer "what colour is the button?": wireframes are greyscale on purpose, so the review stays on flow, content and placement.

Input: $ARGUMENTS

`template.html` holds all styling and behavior and `build.py` fills it. You write only the `<section>` blocks, using the wireframe kit below. The page already provides:
- **Header:** title, where it was drawn from, **Based on** (the repository files you read), **A+** for a shared screen, **Copy feedback**.
- **Section strip** with a status dot per section and "x/y reviewed · x/y picked".
- **Flow:** a numbered row of every screen, built from the screen sections, in the overview.
- **Per section:** verdict buttons (Looks good / Question / Needs change) and a notes box; in a design choice, a **Pick A / Pick B** button on each option.
- **States** become tabs over one wireframe. **Pins** and **callouts** light each other up on hover.
- **Wrap-up:** a tally, every pick, verdict and note, and how to send the feedback back.
- **Keys:** `J`/`K` next/previous, `1` `2` `3` verdict, `A`/`B` pick, `N` notes, `Esc` leave notes.

Verdicts, picks and notes save to the artifact's database by section key, so republishing a revised version keeps them.

## 1. Understand the idea

- **One-line idea:** use it as given.
- **Spec path, or a feature slug** with `~/.claude/feature-work/<slug>/spec.md`: read the spec's goal, users, flows and acceptance criteria. Pass `--job <slug>` to the build.
- Decide who uses it (role), where they start, and what they finish with.

Don't ask questions unless you can't draw anything without the answer; then ask at most three, each with your recommendation. Otherwise **assume** and list each assumption in "Questions to settle", flagged `Assumed`, so the user can overturn it on the page.

## 2. Read the repository (automatic inside one)

When the working directory is a git repository, read it before drawing. Read-only: no servers, installs, builds or tests.
- Find the pages and components the idea touches: route folders, the navigation or sidebar definition, and the page closest to where the feature lives (grep for its title, route or a nearby label).
- Note what a reviewer would recognise: the sidebar items and which is active, the page header (title, breadcrumbs, where its buttons sit), table columns and real row content, filters, how dialogs, drawers, banners, toasts and empty states already look and are worded, and the role names.
- **Reuse what's there.** If the app already has a pattern for this (a dialog, a banner, a filter bar), draw that pattern, with its real wording. Never invent a new pattern where one exists. When two existing patterns would both fit, that's a design choice (step 3).
- Write every file you read to `<scratchpad>/sources.txt`, one repository-relative path per line.

Outside a repository, draw a plain, generic app layout and say so in the overview.

## 3. Map the screens (before writing anything)

Write `<scratchpad>/screens.md`:
- **Screens in flow order.** One per distinct view a person sees: a page, a dialog, a drawer, an email. A dialog over a page is its own screen. Usually 2–6.
- **Changed screens:** for an existing page that changes, draw Before and Now side by side.
- **States** per screen, only those that differ visibly and matter: empty, loading, error, success, no permission, a long list. Most screens need one to three.
- **Design choices: two options, side by side**, wherever there's a real choice a reviewer would want to make: where an entry point lives, a dialog or a separate page, a single action or bulk, inline edit or form. Only real choices, at most three per page; a choice nobody would argue about is just a decision, noted in a callout. Mark your recommended option and say why in one line. If the idea has no real choice, say so in the overview.
- **Callouts:** the decisions a reviewer should notice on each screen: who sees it, when a control is disabled, what is copied or sent, limits, what happens next. Three to six per screen.

## 4. Write the sections

Write them to `<scratchpad>/sections.html` in this order:

| key | attrs | step label | h2 | contents |
|---|---|---|---|---|
| `overview` | | Summary | What this adds | `<p class="lede">`: what the feature lets someone do, one plain sentence. A line on who uses it and where it starts. `<ol class="flow" id="flow"></ol>` (filled automatically). The legend (below). |
| `s-<name>` | `data-screen="Short name"` | leave empty: filled as "Screen n" | the screen's name | One line of context, the wireframe (or `.states`, or `.pair`), then `ol.callouts`. |
| `c-<name>` | `data-choice` | Design choice | the question, e.g. "Where does the export start?" | One line of context, then `.options` with exactly two `figure.option`. |
| `questions` | | Before building | Questions to settle | `ul.points`; each item starts `<span class="flag">Decide</span>` or `<span class="flag assume">Assumed</span>`. |

Put each design choice right after the screen it belongs to. Keys are stable: keep the same keys when you revise, so the user's notes stay attached.

The overview's legend, as is:

```html
<div class="legend"><span><i class="sw"></i>New in this feature</span><span><i class="sw gone"></i>Removed</span><span><i class="pin">1</i>See the note with that number</span></div>
```

### A screen

```html
  <section data-key="s-list" data-screen="Invoices list">
    <div class="content">
      <p class="step"></p>
      <h2>Invoices list</h2>
      <p>Admins start here. The new button sits with the page's other actions.</p>
      <div class="frame" data-url="/admin/invoices">
        <div class="app">
          <nav class="side"><b class="logo">Orbit</b><span>Dashboard</span><span class="on">Invoices</span><span>Customers</span></nav>
          <div class="main">
            <div class="ph"><h4>Invoices</h4><div class="row"><span class="wb">Filter</span><span class="wb pri new">Download CSV</span><i class="pin">1</i></div></div>
            <table class="wt"><tr><th>Number</th><th>Customer</th><th class="num">Amount</th></tr>
              <tr><td>INV-1042</td><td>Desert Palms HOA</td><td class="num">$480.00</td></tr></table>
          </div>
        </div>
      </div>
      <ol class="callouts">
        <li><strong>Only admins</strong> see Download CSV; other roles see the page as it is today.</li>
      </ol>
    </div>
  </section>
```

States, as tabs over one wireframe:

```html
<div class="states">
  <figure class="state" data-label="Default"><div class="frame" data-url="…">…</div></figure>
  <figure class="state" data-label="Empty"><div class="frame" data-url="…">…</div></figure>
</div>
```

Before and Now:

```html
<div class="pair">
  <figure><figcaption>Before</figcaption><div class="frame" data-url="…">…</div></figure>
  <figure><figcaption>Now</figcaption><div class="frame" data-url="…">…</div></figure>
</div>
```

### A design choice

```html
  <section data-key="c-entry" data-choice>
    <div class="content">
      <p class="step">Design choice</p>
      <h2>Where does the export start?</h2>
      <p>Both use patterns the app already has.</p>
      <div class="options">
        <figure class="option" data-option="A" data-label="Button in the page header">
          <div class="opt-head"><h4><b>A</b>Button in the page header</h4><span class="rec">Recommended</span></div>
          <div class="frame" data-url="…">…</div>
          <div class="tradeoffs"><div><h5>Good</h5><ul><li>One click, always visible</li></ul></div><div><h5>Watch</h5><ul><li>Header gets a third button</li></ul></div></div>
        </figure>
        <figure class="option" data-option="B" data-label="Item in the Actions menu">
          <div class="opt-head"><h4><b>B</b>Item in the Actions menu</h4></div>
          …
        </figure>
      </div>
    </div>
  </section>
```

`data-option` is `A` or `B`; `data-label` repeats the option's name (it goes into the copied feedback). Only one option gets `<span class="rec">Recommended</span>`.

### The wireframe kit

Everything inside `.frame` is a drawing. Use `<span>`s, never real buttons or inputs, so nothing on the page pretends to work.

| Piece | Markup |
|---|---|
| Window | `.frame` with `data-url` (the browser bar is added); `.frame.phone` for a phone screen |
| App shell | `.app` > `nav.side` (`b.logo`, `span`, `span.on` for the current page) + `.main` |
| Page header | `.ph` > `h4` (+ `span.crumb` above it) and a `.row` of buttons |
| Layout | `.row` (`.end`, `.between`), `.col`, `.grid2`, `.grid3`, `.card`, `.card.stat` with `<b>` |
| Buttons | `span.wb`, `.wb.pri` (main action), `.wb.ghost` (link-style), `.wb.off` (disabled) |
| Fields | `.fld` > `span.lbl` + `span.in` (placeholder text inside) or `span.sel`; `.in.area`; `span.help`; `span.err-text` |
| Choices | `span.chk` / `.chk.on`, `span.radio` / `.radio.on` |
| Table | `table.wt` with `th`, `td`, `.num` for numbers |
| Tabs | `.wtabs` > `span`, `span.on` |
| Text and images | `span.sk` (`.w30` `.w50` `.w90`) for filler lines, `.ph-img` for a picture, `.badge`, `.badge.solid`, `.muted` |
| Feedback | `.banner` (`.warn`, `.ok`) with `<b>` then text; `.toast` (sits bottom-right of the frame); `span.spinner`; `.empty` for an empty state |
| Overlays | `.overlay` > `.modal` (`h5`, `.body`, `.foot`); `.drawer`; `.menu-pop` with `span`, positioned with `style="top:…;right:…"` inside a `.rel` parent |
| Marks | `.new` on anything this feature adds; `.gone` on anything it removes (in Before); `i.pin` with the callout number, right after the thing it points at |

Writing rules:
- **Real words.** Real page titles, column names, button labels and plausible example rows (from the repository when you read it). `.sk` filler only for text nobody needs to read. No lorem ipsum.
- **Pins:** numbered 1..n in reading order within each section, matching `ol.callouts` one to one. The build warns when they don't.
- **Callouts** are one or two plain sentences: bold the thing, then the rule. "**Download CSV** is disabled while a filter returns no rows."
- **Mark what's new.** Everything the feature adds gets `.new`; existing parts stay plain, so the change stands out.
- Draw only what's needed to place the change: keep the sidebar and header, but three table rows are enough.

## 5. Build and publish

```bash
cd <repository, or anywhere for an idea alone> && python3 ~/.claude/skills/feature-wireframe/build.py --title "Short feature name" --sections <scratchpad>/sections.html [--sources <scratchpad>/sources.txt] [--job <slug>]
```

It checks the sections (unique keys, pins vs callouts, two options per choice), writes `~/.claude/wireframes/<repo>/<slug>.html`, and prints the existing artifact URL if this page has one. Fix any error it reports and build again.

- **Existing URL, published earlier in this conversation:** publish the same file path again. **From an earlier conversation:** read it (`action: "read"`) first, then publish with that `url`. Either way leave out `icon` and `capabilities`.
- **New:** load the `artifact-capabilities` skill. Publish with `icon: "wireframe"`, a one-sentence `description` and `capabilities: {"db": {}, "user": {}}`. Write the URL into the `.url` file the script named (and to `~/.claude/feature-work/<slug>/wireframes.url` with `--job`).
- Reply with the link, the screens in one line, each design choice with your recommendation, and the assumptions to check. Don't repeat the rest of the page.

## 6. Revise from feedback

The user clicks **Copy feedback** and pastes it back. It lists each section by key with its verdict, pick, settled questions and notes.
- Apply it: redraw what was marked Needs change, answer each Question in the section's context line or a callout, and keep the picked option. Once a choice is picked, turn that section into a single screen showing the picked option, or drop it if the screen already shows it, and record the pick in "Questions to settle" as decided.
- Keep every other key the same, rebuild, and republish to the same URL.
- When the wireframes are agreed and a `/feature` job exists, say what changed so the Foreman can carry it into the spec. Don't edit the spec yourself.
