#!/usr/bin/env python3
"""Builds the profile README's SVG cards from the data at the top of this file.

    python scripts/build_assets.py

Each card is written as assets/<name>.svg (GitHub's dark theme) and
assets/<name>-light.svg, and the README picks one with <picture>. The buttons
are theme-neutral and written once.

Screenshots in assets/shots/ are pre-cropped WebP. They are embedded as base64
because an SVG loaded through <img> cannot fetch anything external. Brand marks
in assets/icons/ are Simple Icons (CC0).

Animations start at t=0 and take their delay from values/keyTimes, with the
resting state as the base value, so a renderer that ignores SMIL still shows the
finished card instead of a blank one.
"""
from __future__ import annotations

import base64
import datetime as dt
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
TODAY = dt.date.today()

# ── Data: edit here, then re-run ────────────────────────────────────────────
RELEASE = 'v0.66'
WEEKS = 26
STARTED = dt.date(2026, 3, 29)
COMMITS = '460+'
STATS = [('24', 'MODULES LIVE'), ('158K', 'LINES OF TYPESCRIPT'),
         ('92', 'TEST SUITES IN CI'), (RELEASE, 'WEEKLY RELEASE')]

TOOLS = [  # name, Simple Icons slug, tier
    ('Claude Code', 'claude', 'paid'),
    ('Gemini', 'googlegemini', 'free'),
    ('Next.js', 'nextdotjs', 'oss'),
    ('Supabase', 'supabase', 'free'),
    ('Expo', 'expo', 'free'),
    ('Vitest', 'vitest', 'oss'),
    ('Actions', 'githubactions', 'free'),
    ('Vercel', 'vercel', 'free'),
    ('n8n', 'n8n', 'oss'),
    ('Figma', 'figma', 'free'),
]

ROLES = [  # role, organisation, start, end (None = ongoing)
    ('Freelance Software Engineer', 'Independent', dt.date(2024, 1, 1), dt.date(2026, 5, 1)),
    ('Founder & Sole Engineer', 'ProfitView', STARTED, None),
    ('Full-Stack Developer', 'Poseidon Distribution', dt.date(2026, 5, 18), None),
]

# ── Palette: the portfolio's tokens, and their light-theme twins ────────────
BG, CARD, SUBTLE, LINE, FRAME = '#060606', '#0E0E0E', '#161616', '#1F1F1F', '#2A2A2A'
TEXT, TEXT2, MUTED = '#F5F0E8', '#A09882', '#6B6355'
GOLD, GOLD_LT, GREEN, SHADOW = '#D4AF37', '#E8D48B', '#4ADE80', '#000000'

LIGHT = {
    BG: '#FBF9F3', CARD: '#FFFFFF', SUBTLE: '#F5F1E8', LINE: '#E6DFCF', FRAME: '#D8CFBB',
    TEXT: '#14120E', TEXT2: '#5E5748', MUTED: '#7A7262',
    GOLD: '#957416', GOLD_LT: '#B8912A', GREEN: '#15803D', SHADOW: '#8C7B55',
}
TIER = {'paid': ('PAID', GOLD), 'free': ('FREE TIER', GREEN), 'oss': ('OPEN SOURCE', TEXT2)}

SANS = "'Outfit','Inter',ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace"
EASE = 'calcMode="spline" keySplines="0 0 1 1;.16 1 .3 1"'


# ── Helpers ─────────────────────────────────────────────────────────────────
def esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def tw(s: str, size: float, ls: float = 0, mono: bool = False) -> float:
    """Rough rendered width, good enough to lay out chips and labels."""
    return len(s) * (size * (0.6 if mono else 0.53) + ls)


def timing(delay: float, dur: float) -> str:
    total = delay + dur
    return f'keyTimes="0;{delay / total:.3f};1" dur="{total:.2f}s" fill="freeze"'


def appear(body: str, delay: float, dy: float = 12, dur: float = 0.7) -> str:
    """Fade in, and slide by dy, after `delay` seconds."""
    t = timing(delay, dur)
    return (f'<g><animate attributeName="opacity" values="0;0;1" {t}/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 {dy};0 0" {t} {EASE}/>'
            f'{body}</g>')


def grow_bar(x: float, base: float, w: float, h: float, fill: str, opacity: float, delay: float) -> str:
    return (f'<g transform="translate({x:.2f} {base})"><g>'
            f'<animateTransform attributeName="transform" type="scale" values="1 .001;1 .001;1 1" '
            f'{timing(delay, 0.5)} {EASE}/>'
            f'<rect y="{-h}" width="{w:.2f}" height="{h}" rx="3" fill="{fill}" fill-opacity="{opacity:.2f}"/></g></g>')


def pulse(cx: float, cy: float, color: str, r: float = 4) -> str:
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}">'
            f'<animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="1.5" stroke-opacity="0">'
            f'<animate attributeName="r" values="{r};{r * 3.2:.1f}" dur="2.4s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values=".7;0" dur="2.4s" repeatCount="indefinite"/></circle>')


def arrow(x: float, y: float, size: float = 14) -> str:
    """A gold arrow that nudges right on a loop."""
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;4 0;0 0" '
            f'dur="1.8s" repeatCount="indefinite"/>'
            f'<text x="{x:.1f}" y="{y}" font-family="{SANS}" font-size="{size}" fill="{GOLD}">&#8594;</text></g>')


def chip(x: float, y: float, text: str, color: str, h: float = 24, size: float = 10.5) -> tuple[float, str]:
    w = tw(text, size, 2.4, mono=True) + 22
    return w, (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="none" '
               f'stroke="{color}" stroke-opacity=".45"/>'
               f'<text x="{x + 11:.1f}" y="{y + h / 2 + size * .36:.1f}" font-family="{MONO}" font-size="{size}" '
               f'letter-spacing="2.4" fill="{color}">{esc(text)}</text>')


_paths: dict[str, str] = {}


def icon(slug: str, cx: float, cy: float, size: float, color: str) -> str:
    if slug not in _paths:
        svg = (ASSETS / 'icons' / f'{slug}.svg').read_text(encoding='utf-8')
        _paths[slug] = re.search(r' d="([^"]+)"', svg).group(1)
    return (f'<g transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({size / 24:.3f})">'
            f'<path d="{_paths[slug]}" fill="{color}"/></g>')


def shot(name: str, x: float, y: float, w: float, h: float, cid: str, zoom: bool = False) -> str:
    data = base64.b64encode((ASSETS / 'shots' / name).read_bytes()).decode()
    img = (f'<image href="data:image/webp;base64,{data}" x="{x}" y="{y}" width="{w}" height="{h}" '
           f'preserveAspectRatio="xMidYMid slice"/>')
    if zoom:  # a slow breathe, scaled about the centre
        cx, cy = x + w / 2, y + h / 2
        img = (f'<g transform="translate({cx} {cy})"><g>'
               f'<animateTransform attributeName="transform" type="scale" values="1;1.04;1" dur="18s" '
               f'repeatCount="indefinite"/><g transform="translate({-cx} {-cy})">{img}</g></g></g>')
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath>'
            f'<g clip-path="url(#{cid})">{img}</g>'
            f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="12" fill="none" stroke="{FRAME}"/>')


DEFS = (f'<linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="{GOLD_LT}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{GOLD_LT}" stop-opacity=".9"/>'
        f'<stop offset="1" stop-color="{GOLD_LT}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="ongoing" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".12"/>'
        f'<stop offset="1" stop-color="{GOLD}" stop-opacity=".6"/></linearGradient>'
        f'<radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".16"/>'
        f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
        f'<filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">'
        f'<feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="{SHADOW}" flood-opacity=".6"/></filter>')


def card(w: int, h: int, label: str, body: str) -> str:
    sheen = (f'<rect x="-280" y="0" width="280" height="1.5" fill="url(#sheen)">'
             f'<animate attributeName="x" values="-280;{w}" dur="7s" begin="1.2s" repeatCount="indefinite"/></rect>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>'
            f'<defs>{DEFS}<clipPath id="card"><rect width="{w}" height="{h}" rx="20"/></clipPath></defs>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="{CARD}" stroke="{LINE}"/>'
            f'<g clip-path="url(#card)">{body}{sheen}</g></svg>\n')


_light = re.compile('|'.join(map(re.escape, LIGHT)), re.I)


def write(name: str, svg: str, light: bool = True) -> None:
    variants = [(name, svg)]
    if light:
        variants.append((f'{name}-light', _light.sub(lambda m: LIGHT[m.group(0).upper()], svg)))
    for fname, markup in variants:
        with open(ASSETS / f'{fname}.svg', 'w', encoding='utf-8', newline='\n') as f:
            f.write(markup)
    print(f'{name:<14} {len(svg) / 1024:6.1f} KB')


# ── Cards ───────────────────────────────────────────────────────────────────
def profitview() -> str:
    left = [
        appear(pulse(66, 86, GREEN) + f'<text x="82" y="90.5" font-family="{MONO}" font-size="12" '
               f'letter-spacing="5" fill="{TEXT2}">CURRENTLY BUILDING</text>', .05),
        appear(f'<text x="56" y="150" font-family="{SANS}" font-size="38" font-weight="600" letter-spacing="-.3" '
               f'fill="{TEXT}">ProfitView Accounting</text>', .15),
        appear(f'<text x="56" y="186" font-family="{SANS}" font-size="16.5" fill="{TEXT2}">'
               f'BIR-compliant accounting for Philippine businesses.</text>', .25),
    ]
    x, chips = 56.0, ''
    for label in ('ENTERPRISE SAAS', 'SOLE ENGINEER', f'{STARTED:%b %Y} — NOW'.upper()):
        w, c = chip(x, 208, label, GOLD)
        chips += c
        x += w + 10
    left.append(appear(chips, .35))

    stats = ''.join(
        f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="40" font-weight="600" fill="{GOLD}">{esc(v)}</text>'
        f'<text x="{x}" y="{y + 26}" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{MUTED}">{esc(k)}</text>'
        for (v, k), (x, y) in zip(STATS, [(56, 336), (306, 336), (56, 436), (306, 436)]))
    left.append(appear(f'<rect x="56" y="268" width="480" height="1" fill="{LINE}"/>'
                       f'<rect x="286" y="290" width="1" height="180" fill="{LINE}"/>'
                       f'<rect x="56" y="386" width="480" height="1" fill="{LINE}"/>{stats}', .45))
    left.append(appear(f'<text x="56" y="518" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{GOLD}">'
                       f'VIEW CASE STUDY</text>' + arrow(56 + tw('VIEW CASE STUDY ', 12, 4, True), 518.5), .6))

    screens = (
        f'<ellipse cx="860" cy="290" rx="360" ry="240" fill="url(#glow)"/>'
        + appear(f'<g opacity=".5">{shot("profitview-slsp.webp", 624, 78, 520, 325, "back")}</g>', .2, dy=-14)
        + appear(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" '
                 f'dur="7s" begin="1.6s" repeatCount="indefinite"/><g filter="url(#shadow)">'
                 f'{shot("profitview-dashboard.webp", 572, 152, 540, 338, "front")}</g></g>', .35, dy=22)
    )
    label = 'Currently building ProfitView Accounting: ' + ', '.join(f'{v} {k.lower()}' for v, k in STATS)
    return card(1200, 560, label, screens + ''.join(left))


def work(name: str, shot_name: str, kicker: str, title: str, hook: str, meta: str,
         badge: str, badge_color: str, live: bool = False) -> None:
    # Badge sits on the title row, right-aligned, clear of the screenshot.
    bw = tw(badge, 10.5, 2.4, mono=True) + 22 + (14 if live else 0)
    bx = 568 - bw
    b = (f'<rect x="{bx:.1f}" y="415" width="{bw:.1f}" height="26" rx="13" fill="none" '
         f'stroke="{badge_color}" stroke-opacity=".5"/>')
    if live:
        b += pulse(round(bx + 14.5, 1), 428, badge_color, 3.5)
    b += (f'<text x="{bx + (25 if live else 11):.1f}" y="431.8" font-family="{MONO}" font-size="10.5" '
          f'letter-spacing="2.4" fill="{badge_color}">{esc(badge)}</text>')
    body = (
        appear(shot(shot_name, 24, 24, 552, 330, 'shot', zoom=True), .05, dy=10)
        + appear(b, .5, dy=6)
        + appear(f'<text x="32" y="398" font-family="{MONO}" font-size="11" letter-spacing="4" '
                 f'fill="{GOLD}">{esc(kicker)}</text>', .2)
        + appear(f'<text x="32" y="438" font-family="{SANS}" font-size="28" font-weight="600" letter-spacing="-.2" '
                 f'fill="{TEXT}">{esc(title)}</text>', .28)
        + appear(f'<text x="32" y="470" font-family="{SANS}" font-size="15.5" fill="{TEXT2}">{esc(hook)}</text>', .36)
        + f'<rect x="32" y="494" width="536" height="1" fill="{LINE}"/>'
        + appear(f'<text x="32" y="521" font-family="{MONO}" font-size="10.5" letter-spacing="2.4" '
                 f'fill="{MUTED}">{esc(meta)}</text>'
                 f'<text x="548" y="521" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" '
                 f'fill="{GOLD}">VIEW</text>' + arrow(552, 521.5, 13), .44)
    )
    write(name, card(600, 540, f'{title}: {hook}', body))


def build() -> str:
    o = [appear(f'<text x="56" y="72" font-family="{MONO}" font-size="12" letter-spacing="5" '
                f'fill="{TEXT2}">HOW I BUILD</text>', .05)]

    def phase(x: float, slug: str, name: str, tier: str, caption: str, on: bool, delay: float) -> str:
        label, color = TIER[tier]
        w, c = chip(x + 92, 156, label, color, h=22, size=10)
        return appear(
            f'<rect x="{x}" y="104" width="400" height="92" rx="16" fill="{SUBTLE}" '
            f'stroke="{GOLD if on else LINE}" stroke-opacity="{.5 if on else 1}"/>'
            f'<circle cx="{x + 48}" cy="150" r="27" fill="{BG}" stroke="{GOLD if on else LINE}" '
            f'stroke-opacity="{.35 if on else 1}"/>'
            + icon(slug, x + 48, 150, 24, GOLD if on else TEXT2)
            + f'<text x="{x + 92}" y="143" font-family="{SANS}" font-size="22" font-weight="600" '
              f'fill="{TEXT}">{esc(name)}</text>' + c
            + f'<text x="{x + 104 + w:.1f}" y="171" font-family="{MONO}" font-size="11" letter-spacing="1.5" '
              f'fill="{MUTED}">{esc(caption)}</text>', delay)

    o.append(phase(56, 'googlegemini', 'Gemini', 'free', 'where it started', False, .15))
    o.append(appear(
        f'<text x="598" y="138" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="3" '
        f'fill="{MUTED}">THE SWITCH</text>'
        f'<line x1="476" y1="150" x2="722" y2="150" stroke="{FRAME}" stroke-width="2" stroke-dasharray="4 6"/>'
        f'<path d="M714 143 L724 150 L714 157" fill="none" stroke="{GOLD}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="476" cy="150" r="4" fill="{GOLD}">'
        f'<animate attributeName="cx" values="476;712" dur="2.2s" begin="1s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.8;1" dur="2.2s" begin="1s" '
        f'repeatCount="indefinite"/></circle>', .3, dy=0))
    o.append(phase(744, 'claude', 'Claude Code', 'paid', 'how it ships now', True, .45))

    # One bar per weekly release, brightening toward the current one.
    slot = 1088 / WEEKS
    bw = slot - 6
    o.append(appear(
        f'<text x="56" y="252" font-family="{SANS}" font-size="26" font-weight="600" fill="{TEXT}">'
        f'{WEEKS} weeks. {WEEKS} releases.</text>'
        f'<text x="1144" y="252" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" '
        f'fill="{TEXT2}">{COMMITS} COMMITS · 0 MISSED WEEKS</text>', .55))
    months, prev = '', ''
    for i in range(WEEKS):
        last = i == WEEKS - 1
        x = 56 + i * slot
        o.append(grow_bar(x, 392, bw, 96 if last else 64, GOLD_LT if last else GOLD,
                          1 if last else .22 + .5 * i / (WEEKS - 1), .6 + i * .035))
        month = f'{STARTED + dt.timedelta(weeks=i):%b}'.upper()
        if month != prev:
            months += (f'<text x="{x:.1f}" y="416" font-family="{MONO}" font-size="10.5" letter-spacing="2" '
                       f'fill="{MUTED}">{month}</text>')
            prev = month
    o.append(appear(months + f'<text x="{56 + (WEEKS - 1) * slot + bw / 2:.1f}" y="284" text-anchor="middle" '
                    f'font-family="{MONO}" font-size="11" letter-spacing="1" fill="{GOLD}">{RELEASE}</text>',
                    .9, dy=0))

    # The toolchain, each mark tagged with its cost tier.
    legend, x = '', 1144.0
    for tier in ('oss', 'free', 'paid'):
        label, color = TIER[tier]
        x -= tw(label, 10.5, 2.4, mono=True)
        legend += (f'<text x="{x:.1f}" y="482" font-family="{MONO}" font-size="10.5" letter-spacing="2.4" '
                   f'fill="{TEXT2}">{label}</text><circle cx="{x - 11:.1f}" cy="478.5" r="3.5" fill="{color}"/>')
        x -= 32
    o.append(f'<rect x="56" y="446" width="1088" height="1" fill="{LINE}"/>')
    o.append(appear(f'<text x="56" y="482" font-family="{MONO}" font-size="12" letter-spacing="5" '
                    f'fill="{TEXT2}">THE TOOLCHAIN</text>{legend}', 1.0, dy=0))
    slot = 1088 / len(TOOLS)
    for i, (name, slug, tier) in enumerate(TOOLS):
        cx = 56 + slot * (i + .5)
        o.append(appear(
            icon(slug, cx, 528, 30, GOLD if tier == 'paid' else TEXT2)
            + f'<text x="{cx:.1f}" y="570" text-anchor="middle" font-family="{MONO}" font-size="10.5" '
              f'letter-spacing="1" fill="{TEXT2}">{esc(name)}</text>'
            + f'<circle cx="{cx:.1f}" cy="586" r="3" fill="{TIER[tier][1]}"/>', 1.1 + i * .06))

    label = (f'How I build: started on Gemini (free tier), ships on Claude Code (paid). '
             f'{WEEKS} weekly releases, {COMMITS} commits. Toolchain: ' + ', '.join(t[0] for t in TOOLS))
    return card(1200, 616, label, ''.join(o))


def experience() -> str:
    x0, x1, t0, t1 = 56, 1144, dt.date(2024, 1, 1), dt.date(2027, 1, 1)

    def at(d: dt.date) -> float:
        return x0 + (x1 - x0) * (d - t0).days / (t1 - t0).days

    now = at(TODAY)
    o = [appear(f'<text x="56" y="72" font-family="{MONO}" font-size="12" letter-spacing="5" '
                f'fill="{TEXT2}">EXPERIENCE</text>', .05)]
    grid = ''
    for year in range(t0.year, t1.year):
        gx = at(dt.date(year, 1, 1))
        grid += (f'<rect x="{gx:.1f}" y="100" width="1" height="192" fill="{LINE}"/>'
                 f'<text x="{gx + 8:.1f}" y="318" font-family="{MONO}" font-size="11" letter-spacing="2" '
                 f'fill="{MUTED}">{year}</text>')
    o.append(appear(grid, .1, dy=0))

    for i, (role, org, start, end) in enumerate(ROLES):
        y, xs = 112 + i * 60, at(start)
        w = at(end or TODAY) - xs
        ongoing = end is None
        o.append(f'<rect x="{xs:.1f}" y="{y}" width="{w:.1f}" height="40" rx="8" '
                 f'fill="{"url(#ongoing)" if ongoing else GOLD}" fill-opacity="{1 if ongoing else .12}" '
                 f'stroke="{GOLD}" stroke-opacity="{.6 if ongoing else .35}">'
                 f'<animate attributeName="width" values="0;0;{w:.1f}" {timing(.3 + i * .25, .9)} {EASE}/></rect>')
        inside = w > tw(f'{role} · {org}', 15) + 40
        o.append(appear(
            f'<text x="{xs + 18 if inside else xs - 14:.1f}" y="{y + 25.5}" '
            f'text-anchor="{"start" if inside else "end"}" font-family="{SANS}" font-size="15">'
            f'<tspan font-weight="600" fill="{TEXT}">{esc(role)}</tspan>'
            f'<tspan fill="{TEXT2}"> · {esc(org)}</tspan></text>', .6 + i * .25, dy=0))
        if ongoing:
            o.append(appear(pulse(round(now, 1), y + 20, GOLD_LT), 1.1 + i * .25, dy=0))

    o.append(appear(f'<rect x="{now:.1f}" y="96" width="1" height="196" fill="{GOLD}" fill-opacity=".5"/>'
                    f'<text x="{now:.1f}" y="90" text-anchor="middle" font-family="{MONO}" font-size="10" '
                    f'letter-spacing="3" fill="{GOLD}">NOW</text>', 1.2, dy=0))
    label = 'Experience: ' + '; '.join(
        f'{r} at {o_}, {s:%b %Y} to {"present" if e is None else f"{e:%b %Y}"}' for r, o_, s, e in ROLES)
    return card(1200, 340, label, ''.join(o))


def button(label: str, text: str, filled: bool, w: int = 164, h: int = 48) -> str:
    body = (f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" '
            f'fill="{GOLD if filled else CARD}" stroke="{GOLD}" stroke-opacity="{1 if filled else .55}" '
            f'stroke-width="1.5"/>')
    if filled:
        body += (f'<clipPath id="pill"><rect width="{w}" height="{h}" rx="{h / 2}"/></clipPath>'
                 f'<g clip-path="url(#pill)"><rect x="-70" y="0" width="56" height="{h}" fill="url(#shine)" '
                 f'transform="skewX(-20)"><animate attributeName="x" values="-70;{w + 70}" dur="3.4s" begin="1s" '
                 f'repeatCount="indefinite"/></rect></g>')
    body += (f'<text x="{w / 2}" y="{h / 2 + 5.4}" text-anchor="middle" font-family="{SANS}" font-size="15" '
             f'font-weight="600" letter-spacing=".3" fill="{BG if filled else TEXT}">{text}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}"><title>{label}</title>'
            f'<defs><linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#FFFFFF" stop-opacity=".5"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient></defs>{body}</svg>\n')


if __name__ == '__main__':
    write('header', (ASSETS / 'header.svg').read_text(encoding='utf-8'))
    write('profitview', profitview())
    work('bodytracker', 'bodytracker-scan.webp', 'AI-POWERED PWA', 'Body Tracker',
         'Snap a meal, get the macros — even offline.', 'NEXT.JS 16 · SUPABASE · INDEXEDDB',
         'LIVE', GREEN, live=True)
    work('automation', 'automation-n8n.webp', 'WORKFLOW AUTOMATION', 'Business Automation',
         'CRMs, email and payments wired into one flow.', 'N8N · MAKE · WEBHOOKS · OCR',
         '−60% MANUAL WORK', GOLD)
    write('build', build())
    write('experience', experience())
    write('btn-portfolio', button('Portfolio', 'Portfolio &#8599;', True), light=False)
    write('btn-linkedin', button('LinkedIn', 'LinkedIn', False), light=False)
    write('btn-hire', button('Hire me', 'Hire me', False), light=False)
