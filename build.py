#!/usr/bin/env python3
"""Builds the website from the .tex files in content/ using template.html.

Run locally:   python3 build.py      (needs pandoc)  ->  output in _site/
On GitHub the same script runs automatically after every push.
"""
import pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "_site"
PAIR = re.compile(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", re.S)


def tex_to_html(name):
    path = ROOT / "content" / f"{name}.tex"
    if not path.exists():
        print(f"WARNING: content/{name}.tex not found, section left empty")
        return ""
    r = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "html5", "--wrap=none", "--mathjax"],
        input=path.read_text(encoding="utf-8"), capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit(f"ERROR in content/{name}.tex:\n{r.stderr}")
    if r.stderr.strip():
        print(f"Warnings for content/{name}.tex:\n{r.stderr}")
    return r.stdout.strip()


def strip_p(h):
    return re.sub(r"</?p>", "", h).strip()


def mode_plain(h):
    return h


def mode_cards(h):
    return "\n".join(f'<div class="card"><h4>{t}</h4>{d}</div>' for t, d in PAIR.findall(h))


def mode_tags(h):
    out = []
    for t, d in PAIR.findall(h):
        items = [x.strip() for x in re.sub(r"<[^>]+>", "", d).split(",") if x.strip()]
        tags = "".join(f"<span>{i}</span>" for i in items)
        out.append(f'<div class="card"><h4>{t}</h4><div class="tags">{tags}</div></div>')
    return "\n".join(out)


def mode_timeline(h):
    out = []
    for t, d in PAIR.findall(h):
        d = re.sub(r"<p>(.*?)</p>", r"<h4>\1</h4>", d, count=1, flags=re.S)
        out.append(f'<li><span class="yr">{t}</span>{d}</li>')
    return "\n".join(out)


def mode_pubs(h):
    items = "\n".join(
        f'<li><span class="y">{t}</span><div>{d}</div></li>' for t, d in PAIR.findall(h)
    )
    note = re.sub(r"(?s)<dl>.*?</dl>", "", h).strip()
    return items, (f'<p class="note">{strip_p(note)}</p>' if note else "")


def mode_sections(h):
    parts = re.split(r"<h\d[^>]*>(.*?)</h\d>", h)
    return "\n".join(
        f'<div class="card"><h4>{parts[i]}</h4>{parts[i + 1]}</div>'
        for i in range(1, len(parts) - 1, 2)
    )


def main():
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    fill = {
        "about": mode_plain(tex_to_html("about")),
        "research": mode_cards(tex_to_html("research")),
        "equation": mode_plain(tex_to_html("equation")),
        "skills": mode_tags(tex_to_html("skills")),
        "experience": mode_timeline(tex_to_html("experience")),
        "talks": mode_sections(tex_to_html("talks")),
        "honors": mode_timeline(tex_to_html("honors")),
        "contact": mode_plain(tex_to_html("contact")),
    }
    fill["publications"], fill["publications_note"] = mode_pubs(tex_to_html("publications"))
    for key, value in fill.items():
        html = html.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{\w+\}\}", html)
    if left:
        sys.exit(f"ERROR: unfilled placeholders in template: {left}")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(html, encoding="utf-8")
    for f in ROOT.iterdir():  # copy photos, CV pdf, etc.
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp", ".pdf", ".ico"}:
            shutil.copy(f, OUT / f.name)
    for page, target in {"about": "research", "research": "research", "publications": "publications",
                         "teaching": "experience", "contact": "contact"}.items():
        d = OUT / page
        d.mkdir()
        (d / "index.html").write_text(
            f'<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../#{target}">'
            f'<link rel="canonical" href="../#{target}"><title>Redirecting</title>\n', encoding="utf-8")
    print("Built _site/index.html")


if __name__ == "__main__":
    main()
