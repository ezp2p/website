#!/usr/bin/env python3
"""Draws the feature images in src/assets/img/feature-*.svg.

Run from the repository root:  python3 scripts/feature-images.py

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


def write(name, *args):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"feature-{name}.svg").write_text(svg(*args))


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
