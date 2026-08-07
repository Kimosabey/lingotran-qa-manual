#!/usr/bin/env python3
"""
Verify the Lingotran QA Field Manual before shipping.

  python3 scripts/verify.py

Exits non-zero on any failure so it can gate a commit.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist" / "lingotran-qa-field-manual.html"

PAGE_CEILING = 50
WORDS_PER_PAGE = 480
CODE_LINES_PER_PAGE = 52
TABLE_ROWS_PER_PAGE = 30

# CONTEXT.md D2 targets ~75% tables and code. The floor sat at 0.60, which left a
# 15-point corridor the manual could drift down while every build still printed ok.
# 0.70 keeps a little slack for a prose-heavy edit without licensing a slow slide
# back into a textbook.
STRUCTURED_FLOOR = 0.70

# Hero page figure is written "~20 pages" by hand. Allow drift, catch staleness —
# it read "~40 pages" against a real 19.5 for an entire revision.
HERO_PAGE_TOLERANCE = 5

# Companies that must never appear as subject matter.
# Stack tools (React, Node, Azure, Playwright, ...) are allowed and not listed.
FORBIDDEN = [
    "Microsoft", "Amazon", "Netflix", "Atlassian", "Adobe", "Shopify",
    "Duolingo", "Babbel", "Rosetta", "Coursera", "Udemy", "Contoso", "Fabrikam",
]
# "Google" is permitted only in the phrase "Google Docs" / "Google Fonts".
GOOGLE_OK = re.compile(r"Google (?:Docs|Fonts)")

BALANCED_TAGS = ["details", "table", "tr", "td", "div", "pre", "summary", "p", "script", "style"]

failures = []
notes = []


def fail(msg):
    failures.append(msg)


def ok(msg):
    notes.append(msg)


def main():
    if not DIST.exists():
        print(f"FAIL  {DIST} not found — run scripts/build.sh first")
        return 1

    html = DIST.read_text(encoding="utf-8")

    # ---- structural ----
    if not html.rstrip().endswith("</html>"):
        fail("document does not close with </html>")
    else:
        ok("document closes correctly")

    for tag in BALANCED_TAGS:
        o = len(re.findall(r"<" + tag + r"[ >]", html))
        c = len(re.findall(r"</" + tag + r">", html))
        if o != c:
            fail(f"tag <{tag}> unbalanced: {o} open / {c} close")
    if not any("unbalanced" in f for f in failures):
        ok(f"all {len(BALANCED_TAGS)} tracked tags balanced")

    body_m = re.search(r"<body.*?</body>", html, re.S)
    if not body_m:
        fail("no <body> found")
        return report()
    body = re.sub(r"<(style|script).*?</\1>", "", body_m.group(0), flags=re.S)

    # ---- module wiring ----
    mods = re.findall(r'<details class="mod" id="(m\d+)"', html)
    toc = re.findall(r'href="#(m\d+)"', html)
    if mods != toc:
        fail(f"TOC/module mismatch — modules {mods} vs toc {toc}")
    else:
        ok(f"{len(mods)} modules, TOC in sync")

    # ---- page budget ----
    pres = re.findall(r"<pre.*?</pre>", body, re.S)
    tbls = re.findall(r"<table.*?</table>", body, re.S)
    code_lines = sum(p.count("\n") + 1 for p in pres)
    rows = sum(t.count("<tr") for t in tbls)
    all_words = len(re.sub(r"<[^>]+>", " ", body).split())
    nonprose = sum(len(re.sub(r"<[^>]+>", " ", x).split()) for x in pres + tbls)
    prose_words = all_words - nonprose

    p_prose = prose_words / WORDS_PER_PAGE
    p_code = code_lines / CODE_LINES_PER_PAGE
    p_table = rows / TABLE_ROWS_PER_PAGE
    total = p_prose + p_code + p_table

    if total > PAGE_CEILING:
        fail(f"page count {total:.1f} exceeds ceiling of {PAGE_CEILING}")
    else:
        ok(f"page count {total:.1f} / {PAGE_CEILING}")

    structured_share = (p_code + p_table) / total if total else 0
    if structured_share < STRUCTURED_FLOOR:
        fail(f"only {structured_share:.0%} tables+code — target ~75%, floor "
             f"{STRUCTURED_FLOOR:.0%}; manual is drifting to prose")
    else:
        ok(f"{structured_share:.0%} tables+code")

    # ---- hero facts must match reality (CLAUDE.md 5) ----
    facts = re.search(r'<div class="facts">(.*?)</div>', body, re.S)
    if not facts:
        fail("hero .facts block not found")
    else:
        ftext = re.sub(r"<[^>]+>", " ", facts.group(1))
        m_mod = re.search(r"(\d+)\s+modules", ftext)
        if not m_mod:
            fail("hero does not state a module count")
        elif int(m_mod.group(1)) != len(mods):
            fail(f"hero says {m_mod.group(1)} modules, document has {len(mods)}")
        m_pg = re.search(r"~?\s*(\d+)\s+pages", ftext)
        if not m_pg:
            fail("hero does not state a page count")
        elif abs(int(m_pg.group(1)) - total) > HERO_PAGE_TOLERANCE:
            fail(f"hero says ~{m_pg.group(1)} pages, real count is {total:.1f}")
        if not any("hero" in f for f in failures):
            ok(f"hero facts match ({len(mods)} modules, {total:.0f} pages)")

    # ---- content rules ----
    if re.search(r"LingoTran", html):
        fail("found 'LingoTran' — must be 'Lingotran'")
    else:
        ok("no 'LingoTran' typos")

    text = re.sub(r"<[^>]+>", " ", body)
    for name in FORBIDDEN:
        if re.search(r"\b" + re.escape(name), text):
            fail(f"forbidden reference: {name}")
    stray_google = [m for m in re.finditer(r"Google", text) if not GOOGLE_OK.match(text[m.start():m.start() + 20])]
    if stray_google:
        fail(f"'Google' used outside 'Google Docs/Fonts' ({len(stray_google)}x)")
    if not any("forbidden" in f or "Google" in f for f in failures):
        ok("no competing-product references")

    if "Shashi Kumar" not in text:
        fail("Shashi Kumar missing from examples")
    else:
        ok(f"Shashi Kumar in {len(re.findall('Shashi', text))} places")

    # ---- banned textbook sections (CONTEXT.md D3) ----
    # These four never appear in legitimate prose, so scan the whole document.
    for banned in ["Learning Objectives", "Why This Topic Matters",
                   "Chapter Summary", "Knowledge Check"]:
        if banned.lower() in text.lower():
            fail(f"banned section reintroduced: {banned}")

    # The rest of D3 is banned only *as its own section*. Scan headings alone —
    # "Equivalence partitioning" is legitimate as a technique row in 3.3, and a
    # document-wide scan would fail the build on correct content.
    heads = re.findall(r"<(?:h[1-6]|summary)\b[^>]*>(.*?)</(?:h[1-6]|summary)>", body, re.S)
    head_text = " | ".join(re.sub(r"<[^>]+>", " ", h) for h in heads)
    for banned in ["Business Perspective", "Developer Perspective",
                   "Step-by-Step Process", "Equivalence Partitioning"]:
        if banned.lower() in head_text.lower():
            fail(f"banned section reintroduced as a heading: {banned}")
    if not any("banned" in f for f in failures):
        ok("no banned textbook sections")

    # ---- accessibility guards ----
    if "prefers-reduced-motion" not in html:
        fail("missing prefers-reduced-motion guard")
    if "focus-visible" not in html:
        fail("missing :focus-visible ring")
    if not any("motion" in f or "focus" in f for f in failures):
        ok("reduced-motion + focus-visible present")

    return report()


def report():
    for n in notes:
        print(f"  ok    {n}")
    for f in failures:
        print(f"  FAIL  {f}")
    print()
    if failures:
        print(f"{len(failures)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
