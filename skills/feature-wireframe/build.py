#!/usr/bin/env python3
"""Fill template.html with wireframe sections.

Usage: python3 build.py --title "Invoice CSV export" --sections sections.html
                       [--sources sources.txt] [--job <feature slug>] [--slug <name>]

Run it from the repository the wireframes were drawn from (or anywhere, for an idea
with no repository). Writes ~/.claude/wireframes/<repo or "ideas">/<slug>.html and prints
that path plus the saved artifact URL, if this page has one. With --job it also copies
the page to ~/.claude/feature-work/<job>/wireframes.html for the Foreman.

--sources is a file listing the repository files read to draw the wireframes, one per
line; they show under "Based on" in the header.

Before writing, it checks the sections: unique data-key values, an <h2> in each, each
pin numbered 1..n matching that section's callouts, and two options per design choice.
"""
import argparse, html, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True, help='Feature name; " wireframes" is added')
    ap.add_argument("--sections", required=True, help="File with the <section> blocks")
    ap.add_argument("--sources", help="File listing the repository files read, one per line")
    ap.add_argument("--job", help="Feature slug: also copy to ~/.claude/feature-work/<job>/wireframes.html")
    ap.add_argument("--slug", help="Output name (default: from the title)")
    a = ap.parse_args()

    top = git("rev-parse", "--show-toplevel")
    repo = os.path.basename(top) if top else "ideas"
    branch = git("rev-parse", "--abbrev-ref", "HEAD") if top else None
    slug = a.slug or re.sub(r"[^a-z0-9]+", "-", a.title.lower()).strip("-")

    sections = open(os.path.expanduser(a.sections)).read()
    errors, warnings = check(sections)
    for w in warnings:
        print(f"warning: {w}")
    if errors:
        sys.exit("fix these first:\n  " + "\n  ".join(errors))

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
    meta = f"Low-fidelity wireframes for review before building · {where}"

    page = open(os.path.join(HERE, "template.html")).read()
    for k, v in {
        "{{TITLE}}": f"{a.title} wireframes",
        "{{META}}": meta,
        "{{SOURCES}}": sources_html,
        "{{NOTES_KEY}}": f"wf-{repo}-{slug}-notes",
        "{{SECTIONS}}": sections,
    }.items():
        page = page.replace(k, v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", page)
    if left:
        sys.exit(f"Unfilled placeholders: {left}")

    out_dir = os.path.expanduser(f"~/.claude/wireframes/{repo}")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{slug}.html")
    open(out, "w").write(page)
    url_file = os.path.join(out_dir, f"{slug}.url")
    print(f"file: {out}")
    if a.job:
        job_dir = os.path.expanduser(f"~/.claude/feature-work/{a.job}")
        if not os.path.isdir(job_dir):
            sys.exit(f"no feature folder at {job_dir}")
        shutil.copyfile(out, os.path.join(job_dir, "wireframes.html"))
        print(f"job copy: {job_dir}/wireframes.html")
    print(f"artifact: {open(url_file).read().strip() if os.path.exists(url_file) else '(new, save the URL to ' + url_file + ')'}")


if __name__ == "__main__":
    main()
