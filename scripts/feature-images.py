#!/usr/bin/env python3
"""Draws the site's images:

- src/assets/img/feature-*.svg: the animated picture at the top of each program's page;
- src/assets/img/og-*.png: the cards link previews show (Discord, Slack, Mastodon...), 1200x630;
- src/favicon.ico, src/assets/img/favicon-*.png, src/apple-touch-icon.png: from the logo, src/assets/img/logo.png.

Run from the repository root:  python3 scripts/feature-images.py
The PNGs need Pillow, and Noto Sans (Black and Medium) for their lettering (NOTO below says where).

They follow the ezp2p logo: solid nodes and thick round-capped links that stop short of each node, on a clear ground.
Their colours follow the site's theme (prefers-color-scheme): on the light theme, dark ink with a lime pulse; on the
dark theme, lime nodes like the logo, on olive-grey links with a white pulse. The pulse only ever runs on the links.
Light pulses run along the links (SVG SMIL, so they also move inside an <img>), and stop for people who ask their
system for reduced motion.
"""
import math
from pathlib import Path

W, H = 960, 360
BRAND = "#ccff00"  # the logo's lime, the site's --brand
# (nodes, links, pulse) for each theme
LIGHT_THEME = ("#1b2117", "#1b2117", BRAND)
DARK_THEME = (BRAND, "#5d6a53", "#ffffff")
LINK = 11  # link thickness
GAP = 13  # space between a link's end and a node
SPEED = 300  # pulse speed, px per second
OUT = Path(__file__).resolve().parent.parent / "src" / "assets" / "img"


def link_ends(a, b):
    (x1, y1, r1), (x2, y2, r2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (x1 + ux * (r1 + GAP), y1 + uy * (r1 + GAP)), (x2 - ux * (r2 + GAP), y2 - uy * (r2 + GAP))


def svg(title, nodes, links, routes):
    """nodes: {id: (x, y, r)}; links: [(id, id)]; routes: [([id, id, ...], delay_s)]: a pulse visits each node in turn."""
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">',
        "<style>"
        ".node {{ fill: {0} }} .link {{ stroke: {1} }} .light {{ fill: {2} }} ".format(*LIGHT_THEME)
        + "@media (prefers-color-scheme: dark) {{ .node {{ fill: {0} }} .link {{ stroke: {1} }} .light {{ fill: {2} }} }} ".format(*DARK_THEME)
        + 
        "@media (prefers-reduced-motion: reduce) { .pulse { display: none } }"
        "</style>",
        "<defs>",
        '<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>',
        "</defs>",
        f'<g class="link" stroke-width="{LINK}" stroke-linecap="round">',
    ]
    for a, b in links:
        (x1, y1), (x2, y2) = link_ends(nodes[a], nodes[b])
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    out.append("</g>")
    out.append('<g class="node">')
    for x, y, r in nodes.values():
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
    out.append("</g>")

    # Each pulse runs the visible part of each link, then jumps through the node to the next link, so it looks like
    # light passing through the node and on down the next wire.
    for route, delay in routes:
        segs = [link_ends(nodes[a], nodes[b]) for a, b in zip(route, route[1:])]
        d = " ".join(f"M{s[0]:.1f},{s[1]:.1f} L{e[0]:.1f},{e[1]:.1f}" for s, e in segs)
        length = sum(math.dist(s, e) for s, e in segs)
        run = length / SPEED
        dur = run / 0.8  # it rests, unseen, for the last fifth of each cycle
        out.append(
            f'<g class="pulse" opacity="0">'
            f'<circle class="light" r="15" opacity=".6" filter="url(#glow)"/>'
            f'<circle class="light" r="4.5"/>'
            f'<animateMotion path="{d}" dur="{dur:.2f}s" begin="{delay}s" repeatCount="indefinite" '
            f'calcMode="linear" keyPoints="0;1;1" keyTimes="0;.8;1"/>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.76;.8;1" '
            f'dur="{dur:.2f}s" begin="{delay}s" repeatCount="indefinite"/>'
            f"</g>"
        )
    out.append("</svg>")
    return "\n".join(out) + "\n"


PAGES = {}  # name: (nodes, links), for the preview cards


def write(name, *args):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"feature-{name}.svg").write_text(svg(*args))
    PAGES[name] = (args[1], args[2])


# Puddle: two Puddles, straight to each other.
write(
    "puddle",
    "Two Puddles connected directly",
    {"a": (250, 180, 70), "b": (710, 180, 70)},
    [("a", "b")],
    [(["a", "b"], 0), (["b", "a"], 1.1)],
)

# Levee: a friend's Puddle, the Levee in the middle, and the Puddle behind it.
write(
    "levee",
    "A Puddle reached through its Levee",
    {"friend": (150, 180, 58), "levee": (480, 180, 70), "puddle": (810, 180, 58)},
    [("friend", "levee"), ("levee", "puddle")],
    [(["friend", "levee", "puddle"], 0), (["puddle", "levee", "friend"], 1.6)],
)

# Pond: one hub, members around it, like the logo.
pond = {
    "hub": (480, 180, 74),
    "m1": (300, 82, 30),
    "m2": (650, 70, 40),
    "m3": (705, 225, 22),
    "m4": (610, 305, 28),
    "m5": (290, 285, 42),
    "m6": (235, 170, 18),
}
write(
    "pond",
    "Puddles joined to one Pond",
    pond,
    [("hub", m) for m in pond if m != "hub"],
    [
        (["m1", "hub", "m4"], 0),
        (["m2", "hub", "m5"], 0.9),
        (["m6", "hub", "m3"], 1.7),
        (["m4", "hub", "m2"], 2.6),
        (["m5", "hub", "m1"], 3.4),
    ],
)

# Pool: several hubs (seeders), joined to each other, each with members of its own.
pool = {
    "h1": (215, 150, 46),
    "h2": (470, 95, 40),
    "h3": (735, 160, 48),
    "h4": (500, 265, 42),
    "m1": (95, 75, 18),
    "m2": (90, 255, 24),
    "m3": (345, 30, 14),
    "m4": (610, 30, 18),
    "m5": (870, 70, 20),
    "m6": (875, 280, 26),
    "m7": (345, 320, 20),
    "m8": (650, 330, 14),
}
write(
    "pools",
    "Puddles sharing a Pool between several seeders",
    pool,
    [
        ("h1", "h2"), ("h2", "h3"), ("h3", "h4"), ("h4", "h1"), ("h2", "h4"),
        ("h1", "m1"), ("h1", "m2"), ("h2", "m3"), ("h2", "m4"),
        ("h3", "m5"), ("h3", "m6"), ("h4", "m7"), ("h4", "m8"),
    ],
    [
        (["m1", "h1", "h2", "h3", "m6"], 0),
        (["m5", "h3", "h4", "h1", "m2"], 1.2),
        (["m3", "h2", "h4", "m8"], 2.3),
        (["m7", "h4", "h3", "m5"], 3.1),
        (["m4", "h2", "h1", "m1"], 4.0),
    ],
)
print("wrote", sorted(p.name for p in OUT.glob("feature-*.svg")))


# ---- Link preview cards and favicons (PNG) ----

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

NOTO = Path("/usr/share/fonts/noto")
SITE = OUT.parent.parent  # src/
INK = "#11140d"  # the site's --on-brand: text on lime
CARD_W, CARD_H, SS = 1200, 630, 3  # drawn at 3x and scaled down, for smooth edges
LOGO = OUT / "logo.png"

# What each card says, beside its picture. The default card is for every other page.
CARDS = {
    "default": ("Chat with no servers in the middle.", "Your chats, on your own computer."),
    "puddle": ("Puddle", "Your own chat, on your own computer, with no servers in between."),
    "pond": ("Pond", "A community server with channels, roles and voice, joined from your Puddle."),
    "pools": ("Pools", "A community with no server: its members' Puddles hold it. In development."),
    "levee": ("Levee", "A steady address for a Puddle that can't take connections from the internet."),
}


def font(weight, size):
    return ImageFont.truetype(str(NOTO / f"NotoSans-{weight}.ttf"), size * SS)


def wrap(draw, text, f, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=f) <= width * SS or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def network(draw, nodes, links, box):
    """The page's picture in black, fitted into box (x, y, w, h), as the logo draws it."""
    bx, by, bw, bh = box
    k = min(bw / W, bh / H)
    ox, oy = bx + (bw - W * k) / 2, by + (bh - H * k) / 2

    def pt(x, y):
        return ((ox + x * k) * SS, (oy + y * k) * SS)

    lw = LINK * k * SS
    for a, b in links:
        s, e = link_ends(nodes[a], nodes[b])
        p, q = pt(*s), pt(*e)
        draw.line([p, q], fill=INK, width=round(lw))
        for cx, cy in (p, q):  # round caps
            draw.ellipse([cx - lw / 2, cy - lw / 2, cx + lw / 2, cy + lw / 2], fill=INK)
    for x, y, r in nodes.values():
        cx, cy = pt(x, y)
        rr = r * k * SS
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=INK)


def card(name):
    title, line = CARDS[name]
    img = Image.new("RGB", (CARD_W * SS, CARD_H * SS), BRAND)
    d = ImageDraw.Draw(img)
    pad = 72
    if name in PAGES:
        network(d, *PAGES[name], (600, 120, 540, 390))
    else:
        logo = Image.open(LOGO).convert("RGB").resize((430 * SS, 430 * SS), Image.LANCZOS)
        img.paste(logo, (700 * SS, 100 * SS))

    # the brand, small, top left
    d.text((pad * SS, 64 * SS), "ezp2p", font=font("Black", 40), fill=INK)
    # the title, then the line under it
    tf = font("Black", 76 if name in PAGES else 60)
    y = 190 if name in PAGES else 165
    for t in wrap(d, title, tf, 520):
        d.text((pad * SS, y * SS), t, font=tf, fill=INK)
        y += 84 if name in PAGES else 70
    lf = font("Medium", 32)
    y += 22
    for t in wrap(d, line, lf, 500):
        d.text((pad * SS, y * SS), t, font=lf, fill=INK)
        y += 44
    d.text((pad * SS, (CARD_H - 92) * SS), "www.ezp2p.org", font=font("Medium", 28), fill=INK)
    img.resize((CARD_W, CARD_H), Image.LANCZOS).save(OUT / f"og-{name}.png", optimize=True)


for name in CARDS:
    card(name)

logo = Image.open(LOGO).convert("RGBA")
logo.resize((32, 32), Image.LANCZOS).save(OUT / "favicon-32.png", optimize=True)
logo.resize((192, 192), Image.LANCZOS).save(OUT / "favicon-192.png", optimize=True)
logo.resize((180, 180), Image.LANCZOS).convert("RGB").save(SITE / "apple-touch-icon.png", optimize=True)
logo.save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote", sorted(p.name for p in OUT.glob("og-*.png")), "and the favicons")
