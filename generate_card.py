#!/usr/bin/env python3
"""RAWFORM profile card generator.
Single transparent SVG; text colors flip via prefers-color-scheme.
Usage: generate_card.py --commits N --adds N --dels N [--outdir DIR]
"""
import argparse, html, os

KEYCOL = 15

def kv(key, val):
    return key + "." * (KEYCOL - len(key)), val

STYLE = """<style>
.t{fill:#111111}.m{fill:#6b6b66}.g{fill:#1a7f37}.r{fill:#cf222e}.s{stroke:#c9c9c4}
@media (prefers-color-scheme: dark){
.t{fill:#d7d6d2}.m{fill:#8a8a86}.g{fill:#3fb950}.r{fill:#f85149}.s{stroke:#3a3a3a}
}
</style>"""

def build(art, stats):
    FS = 7.0; CW = FS * 0.55; DY = FS
    art_w = max(len(l) for l in art) * CW
    ix = art_w + 24 + 56
    ILH = 20; IFS = 12.5
    MONO = "Consolas,'Cascadia Mono',ui-monospace,monospace"

    c = stats["commits"]; a = stats["adds"]; d = stats["dels"]
    rows = [
        ("head", "rawform@studios"), ("rule",),
        ("kv", *kv("Studio", '"RAWFORM"')),
        ("kv", *kv("Role", "AI Creative Direction")),
        ("kv", *kv("Est", "2025")),
        ("kv", *kv("Craft", "Campaigns / Creative Direction / Social Content")),
        ("gap",),
        ("kv", *kv("OS", "Windows 11 / macOS 26 Tahoe")),
        ("kv", *kv("IDE", "Antigravity 2.2.1")),
        ("kv", *kv("Output", "Image / Video / UI/UX / Workflows")),
        ("kv", *kv("Direction", "Me")),
        ("kv", *kv("Production", "AI")),
        ("kv", *kv("Stack", "Figma / Claude Code / Higgsfield / Weavy")),
        ("gap",),
        ("head", "Contact"), ("rule",),
        ("kv", *kv("Visit Us", "rawformstudios.com")),
        ("kv", *kv("Email", "hello@rawformstudios.com")),
        ("kv", *kv("Instagram", "@rawfrmm")),
        ("kv", *kv("Pinterest", "@rawfrmm")),
        ("gap",),
        ("head", "My Stats"), ("rule",),
        ("kv", *kv("Commits", f"{c:,}")),
        ("loc", *kv("Lines of Code", "")),
    ]
    y = 40
    for r in rows:
        if r[0] == "gap": y += ILH * 0.6
        elif r[0] == "head": y += 10
        elif r[0] == "rule": y += ILH * 0.85
        else: y += ILH
    art_h = len(art) * DY
    H = int(max(art_h + 40, y + 14))
    W = int(ix + 430)
    art_y0 = (H - art_h) / 2 + DY

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="RAWFORM profile card">']
    s.append(STYLE)
    s.append(f'<text class="t" font-family="{MONO}" font-size="{FS}" xml:space="preserve">')
    yy = art_y0
    for line in art:
        s.append(f'<tspan x="24" y="{yy:.1f}">{html.escape(line)}</tspan>')
        yy += DY
    s.append("</text>")

    y = 40
    for r in rows:
        if r[0] == "gap":
            y += ILH * 0.6
        elif r[0] == "head":
            s.append(f'<text class="t" x="{ix:.0f}" y="{y:.0f}" font-family="{MONO}" font-size="{IFS+1}" font-weight="bold" xml:space="preserve">{r[1]}</text>')
            y += 10
        elif r[0] == "rule":
            s.append(f'<line class="s" x1="{ix:.0f}" y1="{y:.0f}" x2="{ix+400:.0f}" y2="{y:.0f}" stroke-width="1"/>')
            y += ILH * 0.85
        elif r[0] == "loc":
            s.append(
                f'<text x="{ix:.0f}" y="{y:.0f}" font-family="{MONO}" font-size="{IFS}" xml:space="preserve">'
                f'<tspan class="m">{r[1]}</tspan><tspan class="t">  {a - d:,} ( </tspan>'
                f'<tspan class="g">{a:,}++</tspan><tspan class="t"> / </tspan>'
                f'<tspan class="r">{d:,}--</tspan><tspan class="t"> )</tspan></text>')
            y += ILH
        else:
            s.append(
                f'<text x="{ix:.0f}" y="{y:.0f}" font-family="{MONO}" font-size="{IFS}" xml:space="preserve">'
                f'<tspan class="m">{r[1]}</tspan><tspan class="t">  {html.escape(r[2])}</tspan></text>')
            y += ILH
    s.append("</svg>")
    return "\n".join(s)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--commits", type=int, required=True)
    p.add_argument("--adds", type=int, required=True)
    p.add_argument("--dels", type=int, required=True)
    p.add_argument("--outdir", default=".")
    args = p.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "portrait.txt"), encoding="utf-8") as f:
        art = [l.rstrip("\n") for l in f]
    svg = build(art, {"commits": args.commits, "adds": args.adds, "dels": args.dels})
    path = os.path.join(args.outdir, "rawform-card.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", path)

if __name__ == "__main__":
    main()
