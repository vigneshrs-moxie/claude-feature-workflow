#!/usr/bin/env python3
"""Fill template.html with wireframe sections.

Usage: python3 build.py --title "Invoice CSV export" --sections sections.html
                       [--theme theme.css --fonts "Geist,Geist Mono"]
                       [--sources sources.txt] [--job <feature slug>] [--slug <name>]

Run it from the repository the wireframes were drawn from (or anywhere, for an idea
with no repository). Writes ~/.claude/wireframes/<repo or "ideas">/<slug>.html (the page to
publish) and prints that path plus the saved artifact URL, if this page has one.

With --job <slug> (inside a /feature job), it also writes to the job's private folder
($WORKSHOP_FEATURES_DIR or ~/.claude/feature-work, then <slug>/), for the Foreman and the
Feature Workshop dashboard:
  wireframes.html  the same page as a complete document, viewable straight from disk
  wireframes.json  what the page holds (screens, choices, questions), its version and URL
After publishing, record the link (same --slug or --title, and --job if any):
  python3 build.py --record-url <artifact url> --title "Invoice CSV export" [--job <slug>]
It writes <slug>.url next to the page and, with --job, wireframes.url and "url" in wireframes.json.

--sources is a file listing the repository files read to draw the wireframes, one per
line; they show under "Based on" in the header.

--theme makes the page high fidelity: the file is the app's Tailwind v4 theme (its globals.css
trimmed to @custom-variant, @theme, the :root and .dark variables, and base rules scoped to
.canvas). The page compiles it in the browser with Tailwind and loads Lucide icons, so
.frame.hifi screens can use the app's own classes. --fonts names Google Fonts families to load.

Before writing, it checks the sections: unique data-key values, an <h2> in each, each
pin numbered 1..n matching that section's callouts, and two options per design choice.
"""
import argparse, html, json, os, re, subprocess, sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
# Pinned versions of the in-page Tailwind compiler and the icon set.
TAILWIND = "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.1.11"
LUCIDE = "https://cdn.jsdelivr.net/npm/lucide@0.469.0/dist/umd/lucide.min.js"


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def check(sections):
    """Return (errors, warnings) for the sections file."""
    errors, warnings, keys = [], [], []
    blocks = re.split(r"(?=<section\b)", sections)
    for b in blocks:
        m = re.match(r"<section\b[^>]*\bdata-key=\"([^\"]+)\"", b)
        if not m:
            continue
        key = m.group(1)
        if key in keys:
            errors.append(f"data-key \"{key}\" is used twice")
        keys.append(key)
        if "<h2" not in b:
            errors.append(f"{key}: no <h2>")
        drawn = re.sub(r"<div class=\"legend\">.*?</div>", "", b, flags=re.S)  # the legend's sample pin isn't a pin
        pins = [int(n) for n in re.findall(r"class=\"pin[^\"]*\"[^>]*>\s*(\d+)\s*<", drawn)]
        callouts = re.search(r"<ol class=\"callouts\">(.*?)</ol>", b, re.S)
        count = len(re.findall(r"<li\b", callouts.group(1))) if callouts else 0
        if pins and sorted(set(pins)) != list(range(1, count + 1)):
            warnings.append(f"{key}: pins {sorted(set(pins))} don't match {count} callouts")
        if count and not pins:
            warnings.append(f"{key}: {count} callouts but no pins in the wireframe")
        if "data-choice" in re.match(r"<section\b[^>]*>", b).group(0):
            n = len(re.findall(r"class=\"option[\" ]", b))
            if n != 2:
                errors.append(f"{key}: a design choice needs exactly 2 options, found {n}")
    if not keys:
        errors.append("no <section data-key> blocks found")
    return errors, warnings


def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def summary(sections):
    """What the page holds, for the Foreman and the dashboard."""
    out = {"screens": [], "choices": [], "questions": []}
    for b in re.split(r"(?=<section\b)", sections):
        tag = re.match(r"<section\b[^>]*>", b)
        if not tag:
            continue
        attr = dict(re.findall(r"([\w-]+)=\"([^\"]*)\"", tag.group(0)))
        key, h2 = attr.get("data-key"), re.search(r"<h2[^>]*>(.*?)</h2>", b, re.S)
        if "data-screen" in attr:
            views = re.findall(r"class=\"state\"[^>]*data-label=\"([^\"]*)\"", b) or [text(c) for c in re.findall(r"<figcaption[^>]*>(.*?)</figcaption>", b, re.S)]
            out["screens"].append({"key": key, "name": attr["data-screen"], "states": views})
        elif "data-choice" in tag.group(0):
            opts = []
            for o in re.split(r"(?=<figure class=\"option)", b)[1:]:
                oa = dict(re.findall(r"([\w-]+)=\"([^\"]*)\"", re.match(r"<figure[^>]*>", o).group(0)))
                opts.append({"id": oa.get("data-option"), "label": html.unescape(oa.get("data-label", "")), "recommended": 'class="rec"' in o})
            out["choices"].append({"key": key, "question": text(h2.group(1)) if h2 else "", "options": opts})
        elif key == "questions":
            for li in re.findall(r"<li\b[^>]*>(.*?)</li>", b, re.S):
                kind = "assumed" if "flag assume" in li else "decide"
                out["questions"].append({"kind": kind, "text": re.sub(r"^(Decide|Assumed)\s*", "", text(li))})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", help='Feature name; " wireframes" is added')
    ap.add_argument("--sections", help="File with the <section> blocks")
    ap.add_argument("--record-url", help="Only save this published artifact URL for the page (no build)")
    ap.add_argument("--sources", help="File listing the repository files read, one per line")
    ap.add_argument("--job", help="Feature slug: also copy to ~/.claude/feature-work/<job>/wireframes.html")
    ap.add_argument("--slug", help="Output name (default: from the title)")
    ap.add_argument("--theme", help="The app's Tailwind theme CSS; turns on high-fidelity screens")
    ap.add_argument("--fonts", help='Comma-separated Google Fonts families, e.g. "Geist,Geist Mono"')
    a = ap.parse_args()

    if not (a.slug or a.title):
        sys.exit("pass --title (or --slug)")
    top = git("rev-parse", "--show-toplevel")
    repo = os.path.basename(top) if top else "ideas"
    branch = git("rev-parse", "--abbrev-ref", "HEAD") if top else None
    slug = a.slug or re.sub(r"[^a-z0-9]+", "-", a.title.lower()).strip("-")
    out_dir = os.path.expanduser(f"~/.claude/wireframes/{repo}")
    job_dir = None
    if a.job:
        root = os.path.expanduser(os.environ.get("WORKSHOP_FEATURES_DIR") or "~/.claude/feature-work")
        job_dir = os.path.join(root, a.job)
        if not os.path.isdir(job_dir):
            sys.exit(f"no feature folder at {job_dir}")

    if a.record_url:
        if not re.match(r"https://claude\.ai/(code/)?artifact/[\w-]+$", a.record_url):
            sys.exit("--record-url takes a claude.ai artifact link")
        os.makedirs(out_dir, exist_ok=True)
        open(os.path.join(out_dir, f"{slug}.url"), "w").write(a.record_url + "\n")
        print(f"saved: {out_dir}/{slug}.url")
        if job_dir:
            open(os.path.join(job_dir, "wireframes.url"), "w").write(a.record_url + "\n")
            jpath = os.path.join(job_dir, "wireframes.json")
            if os.path.exists(jpath):
                info = json.load(open(jpath))
                info["url"] = a.record_url
                open(jpath, "w").write(json.dumps(info, indent=2) + "\n")
            print(f"saved: {job_dir}/wireframes.url and wireframes.json")
        return
    if not (a.title and a.sections):
        sys.exit("pass --title and --sections")

    sections = open(os.path.expanduser(a.sections)).read()
    errors, warnings = check(sections)
    for w in warnings:
        print(f"warning: {w}")
    if errors:
        sys.exit("fix these first:\n  " + "\n  ".join(errors))

    head_extra = foot_extra = ""
    if "frame hifi" in sections and not a.theme:
        sys.exit("Sections have high-fidelity frames (.frame.hifi) but no --theme was given")
    if a.theme:
        theme = open(os.path.expanduser(a.theme)).read()
        if re.search(r"^\s*@import\b", theme, re.M):
            print("warning: dropped @import lines from the theme (the in-page compiler includes Tailwind itself)")
            theme = re.sub(r"^\s*@import\b[^\n]*\n", "", theme, flags=re.M)
        if re.search(r"(^|[\s,])(html|body)\s*[,{]", theme):
            print("warning: the theme styles html or body; scope those rules to .canvas or they restyle the review page")
        if "</style" in theme:
            sys.exit("The theme contains </style>")
        fonts = ""
        if a.fonts:
            fams = "&".join("family=" + f.strip().replace(" ", "+") + ":wght@400;500;600;700" for f in a.fonts.split(",") if f.strip())
            fonts = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fams}&display=swap">\n'
        head_extra = f'{fonts}<script src="{TAILWIND}"></script>\n<style type="text/tailwindcss">\n{theme}\n</style>'
        foot_extra = f'<script src="{LUCIDE}"></script>'

    sources = []
    if a.sources:
        sources = [l.strip() for l in open(os.path.expanduser(a.sources)) if l.strip()]
    if sources:
        rows = "\n".join(f"            <code>{html.escape(s)}</code>" for s in sources)
        sources_html = (
            '<details class="menu">\n'
            f'          <summary class="btn" title="The repository files these wireframes were drawn from">Based on ({len(sources)})</summary>\n'
            '          <div class="menu-panel">\n'
            f'            <p>Layouts, labels and patterns were taken from these files in <code style="display:inline">{html.escape(repo)}</code>.</p>\n'
            f"{rows}\n"
            "          </div>\n"
            "        </details>")
    else:
        sources_html = ""

    where = (f"Drawn from <code>{html.escape(repo)}</code> on <code>{html.escape(branch)}</code>" if top
             else "Drawn from the idea alone; no repository was read")
    meta = f"{'Screens in the app' + chr(39) + 's own design' if a.theme else 'Low-fidelity wireframes'} for review before building · {where}"

    page = open(os.path.join(HERE, "template.html")).read()
    for k, v in {
        "{{TITLE}}": f"{a.title} wireframes",
        "{{META}}": meta,
        "{{SOURCES}}": sources_html,
        "{{NOTES_KEY}}": f"wf-{repo}-{slug}-notes",
        "{{SECTIONS}}": sections,
        "{{HEAD_EXTRA}}": head_extra,
        "{{FOOT_EXTRA}}": foot_extra,
    }.items():
        page = page.replace(k, v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", page)
    if left:
        sys.exit(f"Unfilled placeholders: {left}")

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{slug}.html")
    open(out, "w").write(page)
    url_file = os.path.join(out_dir, f"{slug}.url")
    print(f"file: {out}")
    url = open(url_file).read().strip() if os.path.exists(url_file) else None
    if job_dir:
        doc = ('<!doctype html><html><head><meta charset="utf-8">'
               '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
               + page + "</body></html>")
        open(os.path.join(job_dir, "wireframes.html"), "w").write(doc)
        jpath = os.path.join(job_dir, "wireframes.json")
        try:
            prev = json.load(open(jpath))
        except (OSError, ValueError):
            prev = {}
        job_url_file = os.path.join(job_dir, "wireframes.url")
        url = url or (open(job_url_file).read().strip() if os.path.exists(job_url_file) else None) or prev.get("url")
        info = {"schema_version": 1, "version": int(prev.get("version", 0)) + 1, "title": a.title,
                "fidelity": "high" if a.theme else "low", "url": url, "page": "wireframes.html",
                "source": out, "repo": top, "built_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                **summary(sections)}
        open(jpath, "w").write(json.dumps(info, indent=2) + "\n")
        print(f"job: {job_dir}/wireframes.html and wireframes.json (version {info['version']})")
    print(f"artifact: {url or '(new, save the URL to ' + url_file + ')'}")


if __name__ == "__main__":
    main()
