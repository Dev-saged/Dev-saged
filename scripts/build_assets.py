#!/usr/bin/env python3
"""Generates every SVG used by README.md into ./assets. Run: python3 scripts/build_assets.py
Icons: brand marks from Simple Icons (CC0), UI glyphs from Lucide (ISC); both bundled in icons.json."""
import json
import pathlib
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
ICONS = json.loads((pathlib.Path(__file__).parent / "icons.json").read_text())

LAT = "'Inter','Segoe UI','SF Pro Display','Helvetica Neue',Arial,sans-serif"
ARF = "'Segoe UI','Noto Sans Arabic','Noto Kufi Arabic','Geeza Pro',Tahoma,Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,monospace"

LS_TIGHT = 'letter-spacing="-0.5"'
LS_TIGHT1 = 'letter-spacing="-1"'
LS_WIDE = 'letter-spacing="3"'
INK = "#E8EEFF"
MUTED = "#8FA0C2"
PANEL = "#0E1630"
PANEL2 = "#121C3C"
EDGE = "#24325C"

ACCENTS = {
    "violet": ("#8B5CF6", "#6366F1"),
    "amber": ("#F59E0B", "#F97316"),
    "rose": ("#F43F5E", "#EC4899"),
    "cyan": ("#06B6D4", "#3B82F6"),
    "teal": ("#14B8A6", "#10B981"),
    "green": ("#22C55E", "#84CC16"),
    "crimson": ("#E11D48", "#F59E0B"),
    "blue": ("#3B82F6", "#6366F1"),
    "gold": ("#FACC15", "#F59E0B"),
}


def tw(text, size, bold=False, ar=False):
    k = 0.5 if ar else (0.6 if bold else 0.56)
    return len(text) * size * k


def lum(hexc):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def brand(slug, x, y, size, color=None):
    b = ICONS["brand"][slug]
    c = color or "#" + b["hex"]
    if not color and lum(c) < 0.28:
        c = INK
    return f'<path transform="translate({x} {y}) scale({size / 24:.4f})" d="{b["d"]}" fill="{c}"/>'


def lu(name, x, y, size, color, sw=2):
    return (f'<g transform="translate({x} {y}) scale({size / 24:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS["lucide"][name]}</g>')


def text(x, y, s, size, fill=INK, weight=400, anchor="start", family=LAT, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def svg(w, h, body, defs="", style="", title=""):
    t = f"<title>{escape(title)}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'{t}<defs>{defs}</defs><style>{style}@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>'
            f'{body}</svg>')


def grad(gid, c1, c2, x1=0, y1=0, x2=1, y2=1):
    return (f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


def write(path, content):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# ───────────────────────── banner ─────────────────────────
def build_banner():
    W, H = 1200, 420
    roles = [
        "Arabic AI & automation tools",
        "Offline-first systems for the field",
        "Built end-to-end from a phone",
        "Private by design, tested in the open",
    ]
    defs = (
        grad("bg", "#070B1A", "#0F1A3D") + grad("nm", "#FFFFFF", "#9CC4FF", 0, 0, 1, 0)
        + grad("nm2", "#9CC4FF", "#C4B5FD", 0, 0, 1, 0)
        + grad("ph", "#3B82F6", "#8B5CF6") + grad("scr", "#0E1630", "#0A1024", 0, 0, 0, 1)
        + '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
        + '<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#2A3A6E" opacity=".55"/></pattern>'
        + '<clipPath id="clip"><rect width="1200" height="420" rx="26"/></clipPath>'
    )
    style = (
        f".t{{font-family:{LAT}}}"
        "@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-26px)}}"
        "@keyframes drift2{0%,100%{transform:translate(0,0)}50%{transform:translate(-46px,30px)}}"
        "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}"
        "@keyframes swap{0%{opacity:0;transform:translateY(10px)}4%{opacity:1;transform:translateY(0)}"
        "21%{opacity:1;transform:translateY(0)}25%{opacity:0;transform:translateY(-10px)}100%{opacity:0}}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}"
        ".o1{animation:drift 14s ease-in-out infinite}.o2{animation:drift2 17s ease-in-out infinite}"
        ".b1{animation:bob 5s ease-in-out infinite}.b2{animation:bob 6s ease-in-out -2s infinite}"
        ".b3{animation:bob 5.5s ease-in-out -1s infinite}.b4{animation:bob 6.5s ease-in-out -3.5s infinite}"
        ".r{opacity:0;animation:swap 16s infinite}.r2{animation-delay:4s}.r3{animation-delay:8s}.r4{animation-delay:12s}"
        ".dot{animation:pulse 2s ease-in-out infinite}"
        "@media (prefers-reduced-motion: reduce){.r{opacity:0}.r1{opacity:1!important}}"
    )
    b = ['<g clip-path="url(#clip)">', f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dots)"/>',
         '<g filter="url(#blur)"><circle class="o1" cx="180" cy="90" r="190" fill="#2563EB" opacity=".42"/>'
         '<circle class="o2" cx="1010" cy="120" r="210" fill="#7C3AED" opacity=".38"/>'
         '<circle class="o1" cx="640" cy="440" r="170" fill="#06B6D4" opacity=".26"/></g>']
    # text block
    b.append(f'<rect x="68" y="76" width="232" height="30" rx="15" fill="#1B2A5A" stroke="#3B5BB5" stroke-opacity=".6"/>')
    b.append(lu("sparkles", 82, 83, 16, "#9CC4FF"))
    b.append(text(104, 96, "SOFTWARE ARCHITECT", 12.5, "#BFD4FF", 700, extra='letter-spacing="2"'))
    b.append(text(66, 178, "Sajed Al-Abadlah", 72, "url(#nm)", 800, extra='letter-spacing="-1.5"'))
    b.append(text(70, 232, "ساجد العبادلة", 38, "url(#nm2)", 700, family=ARF))
    roles_svg = ""
    for i, r in enumerate(roles, 1):
        roles_svg += text(100, 292, r, 27, "#CFE0FF", 500, extra=f'class="r r{i}"')
    b.append(lu("terminal-square", 68, 270, 26, "#60A5FA"))
    b.append(roles_svg)
    # location chip + flag
    b.append('<rect x="68" y="326" width="206" height="38" rx="19" fill="#0B1330" stroke="#2C3E75"/>')
    b.append(lu("map-pin", 84, 335, 20, "#34D399"))
    b.append(text(112, 351, "Palestine · Gaza", 15, INK, 600))
    b.append('<circle class="dot" cx="254" cy="345" r="5" fill="#34D399"/>')
    b.append('<rect x="290" y="326" width="176" height="38" rx="19" fill="#0B1330" stroke="#2C3E75"/>')
    b.append(lu("smartphone", 306, 335, 20, "#A78BFA"))
    b.append(text(334, 351, "Mobile-first", 15, INK, 600))
    # phone
    px, py = 905, 40
    b.append(f'<g class="b1"><g transform="translate({px} {py})">'
             '<rect x="-6" y="-6" width="212" height="352" rx="40" fill="url(#ph)" opacity=".5"/>'
             '<rect width="200" height="340" rx="34" fill="#0A1024" stroke="url(#ph)" stroke-width="3"/>'
             '<rect x="10" y="10" width="180" height="320" rx="26" fill="url(#scr)"/>'
             '<rect x="74" y="18" width="52" height="10" rx="5" fill="#1B2A5A"/>'
             '<rect x="26" y="44" width="92" height="12" rx="6" fill="#3B82F6"/>'
             '<rect x="26" y="64" width="60" height="8" rx="4" fill="#2B3B6E"/>'
             '<rect x="26" y="92" width="148" height="56" rx="14" fill="#14214A" stroke="#2C3E75"/>'
             '<rect x="36" y="104" width="30" height="30" rx="9" fill="#8B5CF6"/>'
             '<rect x="76" y="107" width="76" height="8" rx="4" fill="#9CB2E6"/><rect x="76" y="123" width="48" height="7" rx="3.5" fill="#3A4E86"/>'
             '<rect x="26" y="158" width="148" height="56" rx="14" fill="#14214A" stroke="#2C3E75"/>'
             '<rect x="36" y="170" width="30" height="30" rx="9" fill="#14B8A6"/>'
             '<rect x="76" y="173" width="66" height="8" rx="4" fill="#9CB2E6"/><rect x="76" y="189" width="54" height="7" rx="3.5" fill="#3A4E86"/>'
             '<rect x="26" y="224" width="148" height="56" rx="14" fill="#14214A" stroke="#2C3E75"/>'
             '<rect x="36" y="236" width="30" height="30" rx="9" fill="#F59E0B"/>'
             '<rect x="76" y="239" width="80" height="8" rx="4" fill="#9CB2E6"/><rect x="76" y="255" width="40" height="7" rx="3.5" fill="#3A4E86"/>'
             '<rect x="62" y="304" width="76" height="6" rx="3" fill="#2B3B6E"/>'
             '</g></g>')

    def float_chip(cls, x, y, icon, label, color, w):
        return (f'<g class="{cls}"><g transform="translate({x} {y})"><rect width="{w}" height="40" rx="20" fill="#0B1330" '
                f'stroke="{color}" stroke-opacity=".7"/>{lu(icon, 14, 9, 22, color)}'
                f'{text(44, 26, label, 14, INK, 600)}</g></g>')

    b.append(float_chip("b2", 742, 96, "wifi-off", "Offline", "#34D399", 116))
    b.append(float_chip("b3", 1062, 150, "sparkles", "Gemini AI", "#A78BFA", 128))
    b.append(float_chip("b4", 724, 300, "languages", "RTL native", "#60A5FA", 134))
    b.append(float_chip("b1", 1076, 292, "shield-check", "Private", "#F59E0B", 112))
    # palestine stripe
    sh = 5
    b.append(f'<rect y="{H - 3 * sh}" width="{W}" height="{sh}" fill="#0B0B0B"/><rect y="{H - 2 * sh}" width="{W}" height="{sh}" fill="#F4F4F4"/>'
             f'<rect y="{H - sh}" width="{W}" height="{sh}" fill="#0F9D58"/><path d="M0 {H - 3 * sh} L40 {H - 1.5 * sh} L0 {H} Z" fill="#E4312B"/>')
    b.append('</g>')
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="26" fill="none" stroke="#2C3E75"/>')
    write("banner.svg", svg(W, H, "".join(b), defs, style, "Sajed Al-Abadlah — Software Architect"))


# ───────────────────────── nav + contact ─────────────────────────
def build_nav():
    items = [("projects", "Projects", "rocket", "#8B5CF6"), ("stack", "Stack", "layers", "#06B6D4"),
             ("principles", "Principles", "shield-check", "#22C55E"), ("contact", "Contact", "mail", "#F59E0B")]
    for slug, label, icon, c in items:
        w = 44 + tw(label, 15, True) + 20
        w = int(w)
        body = (f'<rect x=".5" y=".5" width="{w - 1}" height="42" rx="21" fill="{PANEL}" stroke="{c}" stroke-opacity=".55"/>'
                f'{lu(icon, 16, 11, 20, c)}{text(44, 27.5, label, 15, INK, 600)}')
        write(f"nav-{slug}.svg", svg(w, 44, body, "", "", label))


CONTACTS = [
    ("instagram", "Instagram", "@sajedd.0", "https://instagram.com/sajedd.0", ("#F58529", "#DD2A7B", "#8134AF")),
    ("facebook", "Facebook", "saged.t", "https://facebook.com/saged.t", ("#1877F2", "#1877F2", "#1877F2")),
    ("whatsapp", "WhatsApp", "Message me", "https://wa.me/972597857250", ("#25D366", "#25D366", "#25D366")),
    ("x", "X", "@saged_al", "https://x.com/saged_al", ("#2B2F3A", "#2B2F3A", "#2B2F3A")),
    ("github", "GitHub", "@Dev-saged", "https://github.com/Dev-saged", ("#30363D", "#30363D", "#30363D")),
]


def build_contact():
    for slug, name, handle, _, cols in CONTACTS:
        w, h = 188, 60
        d = (f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{cols[0]}"/>'
             f'<stop offset=".55" stop-color="{cols[1]}"/><stop offset="1" stop-color="{cols[2]}"/></linearGradient>'
             + grad("e", EDGE, cols[1] if slug not in ("x", "github") else "#4A5A8C", 0, 0, 1, 1))
        body = (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="{PANEL}" stroke="url(#e)"/>'
                f'<rect x="9" y="9" width="42" height="42" rx="13" fill="url(#g)"/>'
                f'{brand(slug, 18, 18, 24, "#FFFFFF")}'
                f'{text(62, 28, name, 16, INK, 700)}{text(62, 46, handle, 12.5, MUTED, 500)}')
        write(f"contact-{slug}.svg", svg(w, h, body, d, "", name))


# ───────────────────────── section headers ─────────────────────────
def header(slug, num, en, sub, ar, icon, c1, c2):
    W, H = 1000, 100
    d = grad("a", c1, c2) + grad("l", c1, c2, 0, 0, 1, 0) + grad("pn", PANEL2, "#0A1228", 0, 0, 1, 0)
    d += f'<clipPath id="cp"><rect width="{W}" height="{H}" rx="24"/></clipPath>'
    style = ("@keyframes slide{0%{stroke-dashoffset:0}100%{stroke-dashoffset:-260}}"
             ".run{stroke-dasharray:90 170;animation:slide 4s linear infinite}")
    b = (f'<g clip-path="url(#cp)"><rect width="{W}" height="{H}" fill="url(#pn)"/>'
         f'<circle cx="{W - 40}" cy="0" r="130" fill="{c1}" opacity=".10"/>'
         f'<line x1="0" y1="97" x2="{W}" y2="97" stroke="#1D2B55" stroke-width="6"/>'
         f'<line class="run" x1="0" y1="97" x2="{W}" y2="97" stroke="url(#l)" stroke-width="6"/></g>'
         f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="none" stroke="{EDGE}"/>'
         f'<rect x="22" y="20" width="56" height="56" rx="17" fill="url(#a)"/>{lu(icon, 35, 33, 30, "#FFFFFF", 2)}'
         f'{text(98, 46, en, 30, INK, 800, extra=LS_TIGHT)}'
         f'{text(99, 70, sub, 14, MUTED, 500)}'
         f'{text(W - 26, 46, ar, 28, c1, 800, "end", ARF)}'
         f'{text(W - 26, 70, num, 12.5, MUTED, 700, "end", MONO, LS_WIDE)}')
    write(f"h-{slug}.svg", svg(W, H, b, d, style, en))


def build_headers():
    header("about", "01 / ABOUT", "About", "Who I am and how I build", "نبذة", "user", *ACCENTS["blue"])
    header("projects", "02 / WORK", "Featured Projects", "Real products, shipped and documented", "أبرز المشاريع", "rocket", *ACCENTS["violet"])
    header("stack", "03 / STACK", "Tech Stack", "Tools I reach for every day", "التقنيات", "layers", *ACCENTS["cyan"])
    header("principles", "04 / CRAFT", "How I Build", "Principles behind every project", "فلسفة العمل", "shield-check", *ACCENTS["green"])
    header("contact", "05 / CONTACT", "Let's Talk", "Pick the channel you prefer", "تواصل معي", "mail", *ACCENTS["amber"])
    header("metrics", "06 / LIVE", "GitHub Metrics", "Live from the GitHub API", "إحصائيات", "star", *ACCENTS["rose"])


# ───────────────────────── stats strip ─────────────────────────
def build_stats():
    W, H = 1000, 150
    tiles = [("12", "Featured projects", "مشروعاً مميزاً", "boxes", "#8B5CF6"),
             ("6", "Offline-first systems", "أنظمة تعمل بلا إنترنت", "wifi-off", "#14B8A6"),
             ("AR · EN", "Bilingual interfaces", "واجهات ثنائية اللغة", "languages", "#3B82F6"),
             ("100%", "Built on a phone", "مبنية من الجوال", "smartphone", "#F59E0B")]
    gap = 20
    tile = (W - 3 * gap) / 4
    d = "".join(grad(f"t{i}", c, "#FFFFFF", 0, 0, 1, 1) for i, (*_, c) in enumerate(tiles))
    d += f'<clipPath id="ct"><rect width="{tile}" height="{H}" rx="22"/></clipPath>'
    b = []
    for i, (val, en, ar, icon, c) in enumerate(tiles):
        x = i * (tile + gap)
        b.append(f'<g transform="translate({x} 0)"><g clip-path="url(#ct)"><rect width="{tile}" height="{H}" fill="{PANEL}"/>'
                 f'<rect width="{tile}" height="6" fill="{c}"/></g>'
                 f'<rect x=".5" y=".5" width="{tile - 1}" height="{H - 1}" rx="22" fill="none" stroke="{EDGE}"/>'
                 f'{lu(icon, tile - 48, 26, 26, c)}'
                 f'{text(24, 82, val, 44, "url(#t%d)" % i, 800, extra=LS_TIGHT1)}'
                 f'{text(24, 112, en, 14, INK, 600)}{text(24, 134, ar, 13.5, MUTED, 500, family=ARF)}</g>')
    write("stats.svg", svg(W, H, "".join(b), d, "", "Highlights"))


# ───────────────────────── project cards ─────────────────────────
PROJECTS = [
    # slug, title, ar, repo, accent, icon, tag, l1, l2, chips, featured
    ("lakta", "Lakta Studio AI", "استوديو لقطة", "Lakta-Studio-AI", "violet", "video", "v34.15",
     "Turns long episodes into ready Shorts & Reels:", "AI picks moments, edits, adds Arabic captions.",
     [("b", "python", "Python"), ("b", "ffmpeg", "FFmpeg"), ("b", "googlegemini", "Gemini"), ("b", "telegram", "Telegram")], True),
    ("sawan", "Sawan Kids Story Studio", "استوديو ساجد للقصص", "sawan-kids-story-studio", "amber", "book-open", "v3.4",
     "One idea in, an illustrated, narrated kids' story", "out, in Arabic or English. Offline-ready PWA.",
     [("b", "react", "React"), ("b", "typescript", "TypeScript"), ("b", "googlegemini", "Gemini"), ("b", "pwa", "PWA")], True),
    ("social", "Social Manager", "مدير حساباتي", "social-manager", "rose", "share-2", "",
     "Write once, publish to 7 platforms on schedule", "and auto-reply to comments. Runs on your phone.",
     [("b", "flask", "Flask"), ("b", "sqlite", "SQLite"), ("b", "android", "Android"), ("b", "googlegemini", "Gemini")], False),
    ("bulldozer", "Bulldozer Social", "بلدوزر سوشيل", "bulldozer-social", "gold", "megaphone", "AGPL-3.0",
     "Postiz fork for scheduling, with a built-in", "comment-to-DM auto-reply engine for Instagram.",
     [("b", "typescript", "TypeScript"), ("b", "temporal", "Temporal"), ("b", "instagram", "Instagram")], False),
    ("release", "Release Manager Pro", "مدير الإصدارات الذكي", "release-manager-pro", "cyan", "git-pull-request", "v2.6",
     "Diffs your code, lets Gemini write the release", "notes, then ships to GitHub in one tap.",
     [("b", "javascript", "JavaScript"), ("b", "googlegemini", "Gemini"), ("b", "github", "GitHub"), ("b", "android", "Android")], False),
    ("sms", "Local SMS Parser", "معالج رسائل SMS", "local-sms-parser", "blue", "message-square-text", "",
     "Turns Excel rosters into personalised SMS", "batches. 100% in-browser, nothing uploaded.",
     [("b", "javascript", "JavaScript"), ("b", "html5", "HTML5"), ("b", "css", "CSS")], False),
    ("grcs", "Gaza Refugee Camps System", "منظومة مخيمات النزوح", "wasla-system", "teal", "tent", "v3.0",
     "Offline-first registry for displacement camps,", "live sync across devices. Android + PWA.",
     [("b", "javascript", "JavaScript"), ("b", "firebase", "Firestore"), ("b", "cloudflare", "Workers"), ("b", "pwa", "PWA")], True),
    ("ghiras", "Ghiras Al-Khair", "غراس الخير", "ghiras-alkhair", "green", "heart-handshake", "",
     "Orphan-care management for charities: files,", "sponsorships, reports, roles, encrypted data.",
     [("b", "html5", "HTML5"), ("b", "javascript", "JavaScript"), ("b", "openjdk", "Java"), ("b", "android", "Android")], False),
    ("mushajjir", "Mushajjir", "مُشَجِّر · شجرة العائلة", "Mushajjir", "crimson", "network", "v1.2",
     "Arabic family-tree builder: 3 layouts, 8 export", "formats, 4,000+ people at 60fps, 56 self-tests.",
     [("b", "javascript", "JavaScript"), ("b", "android", "Android"), ("l", "test-tube-diagonal", "56 tests")], False),
    ("aid", "Offline Aid Manager", "نظام إدارة الإغاثة", "offline-aid-manager", "blue", "package-open", "",
     "Beneficiary roster manager for field relief", "work. CSV in/out, data never leaves the device.",
     [("b", "javascript", "JavaScript"), ("b", "html5", "HTML5"), ("b", "css", "CSS")], False),
    ("anira", "Anira", "أنيرا · تسجيل الإنابات", "Anabat", "violet", "clipboard-list", "v1.4",
     "Humanitarian proxy registration with duplicate", "detection, Excel/PDF export, Telegram backup.",
     [("b", "javascript", "JavaScript"), ("b", "telegram", "Telegram"), ("b", "android", "Android")], False),
    ("daftar", "Daftar", "دفتر · إدارة الديون", "daftar", "amber", "notebook-pen", "v1.0",
     "Debt ledger for three shop branches: offline,", "Firebase sync, 80mm thermal receipts.",
     [("b", "javascript", "JavaScript"), ("b", "firebase", "Firebase"), ("b", "android", "Android")], False),
]


def build_cards():
    W, H = 480, 222
    for slug, title, ar, repo, acc, icon, tag, l1, l2, chips, featured in PROJECTS:
        c1, c2 = ACCENTS[acc]
        d = grad("a", c1, c2) + grad("p", PANEL2, "#0A1228", 0, 0, 0, 1) + grad("top", c1, c2, 0, 0, 1, 0)
        style = ("@keyframes shine{0%{transform:translateX(-520px)}100%{transform:translateX(520px)}}"
                 ".sh{animation:shine 6s ease-in-out infinite}")
        b = [f'<clipPath id="c"><rect width="{W}" height="{H}" rx="20"/></clipPath>',
             f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#p)"/>',
             f'<rect width="{W}" height="4" fill="url(#top)"/>',
             f'<circle cx="{W - 30}" cy="-10" r="120" fill="{c1}" opacity=".10"/>',
             f'<rect class="sh" x="0" y="0" width="90" height="{H}" fill="#FFFFFF" opacity=".035" transform="skewX(-18)"/></g>',
             f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="{EDGE}"/>',
             f'<rect x="22" y="24" width="56" height="56" rx="16" fill="url(#a)"/>',
             lu(icon, 36, 38, 28, "#FFFFFF"),
             text(94, 44, title, 20, INK, 800, extra='letter-spacing="-0.3"'),
             text(94, 68, ar, 15, c1, 600, family=ARF)]
        right = W - 22
        if tag:
            tww = int(tw(tag, 12, True) + 22)
            b.append(f'<rect x="{right - tww}" y="14" width="{tww}" height="22" rx="11" fill="{c1}" fill-opacity=".16" stroke="{c1}" stroke-opacity=".6"/>')
            b.append(text(right - tww / 2, 29.5, tag, 12, INK, 700, "middle", MONO))
        if featured:
            b.append(lu("star", right - 18, 192, 16, "#FACC15"))
        b.append(text(22, 108, l1, 14, "#C4D2F5", 500))
        b.append(text(22, 128, l2, 14, "#C4D2F5", 500))
        b.append(f'<line x1="22" y1="146" x2="{W - 22}" y2="146" stroke="#1D2B55"/>')
        cx = 22
        for kind, key, label in chips:
            cw = int(22 + 18 + tw(label, 12.5, True) + 6)
            if cx + cw > W - 22:
                break
            b.append(f'<rect x="{cx}" y="158" width="{cw}" height="28" rx="14" fill="#0A1230" stroke="{EDGE}"/>')
            b.append(brand(key, cx + 10, 165, 14) if kind == "b" else lu(key, cx + 10, 165, 14, "#34D399"))
            b.append(text(cx + 30, 176.5, label, 12.5, INK, 600))
            cx += cw + 8
        b.append(text(22, 208, f"github.com/Dev-saged/{repo}", 11.5, MUTED, 500, family=MONO))
        b.append(text(right - (22 if featured else 0), 208, "Open  ↗", 12.5, c1, 700, "end"))
        write(f"cards/{slug}.svg", svg(W, H + 14, "".join(b), d, style, f"{title} — {ar}"))


# ───────────────────────── stack ─────────────────────────
STACK = [
    ("Languages", "اللغات", [("javascript", "JavaScript"), ("typescript", "TypeScript"), ("python", "Python"), ("kotlin", "Kotlin"),
                             ("html5", "HTML5"), ("css", "CSS")]),
    ("Frameworks & runtime", "الأطر", [("react", "React"), ("vite", "Vite"), ("tailwindcss", "Tailwind"), ("flask", "Flask"),
                                       ("nodedotjs", "Node.js"), ("express", "Express")]),
    ("AI & APIs", "الذكاء والواجهات", [("googlegemini", "Gemini"), ("claude", "Claude"), ("anthropic", "Anthropic API"),
                                        ("telegram", "Telegram Bot"), ("github", "GitHub API")]),
    ("Platform & data", "المنصات والبيانات", [("android", "Android"), ("pwa", "PWA"), ("firebase", "Firebase"), ("cloudflare", "Cloudflare"),
                                              ("githubactions", "Actions"), ("ffmpeg", "FFmpeg"), ("sqlite", "SQLite"),
                                              ("postgresql", "PostgreSQL"), ("temporal", "Temporal"), ("docker", "Docker")]),
]


def build_stack():
    W = 1000
    y = 0
    b = []
    for en, ar, items in STACK:
        # layout chips
        x0, x, rowy, rows = 250, 250, 0, 1
        placed = []
        for slug, label in items:
            cw = int(22 + 22 + tw(label, 14, True) + 8)
            if x + cw > W:
                x, rowy, rows = x0, rowy + 50, rows + 1
            placed.append((slug, label, x, rowy, cw))
            x += cw + 10
        gh = max(rows * 50 + 22, 92)
        b.append(f'<g transform="translate(0 {y})"><rect x=".5" y=".5" width="{W - 1}" height="{gh - 1}" rx="22" fill="{PANEL}" stroke="{EDGE}"/>')
        b.append(text(26, 40, en, 16, INK, 800))
        b.append(text(26, 62, ar, 14, MUTED, 500, family=ARF))
        for slug, label, px, py, cw in placed:
            b.append(f'<rect x="{px}" y="{py + 14}" width="{cw}" height="38" rx="19" fill="#0A1230" stroke="{EDGE}"/>')
            b.append(brand(slug, px + 14, py + 24, 18))
            b.append(text(px + 40, py + 38.5, label, 14, INK, 600))
        b.append("</g>")
        y += gh + 16
    write("stack.svg", svg(W, y - 16, "".join(b), "", "", "Tech stack"))


# ───────────────────────── principles ─────────────────────────
def build_principles():
    items = [("wifi-off", "Offline-first", "تعمل بلا إنترنت",
              "Local storage first, then sync when the network returns.", "Field conditions are the default, not the edge case.", "teal"),
             ("shield-check", "Private by design", "الخصوصية أولاً",
              "Sensitive data stays on the device, encrypted wherever", "it has to sync. No trackers, no pointless accounts.", "violet"),
             ("languages", "Arabic-native", "عربي أصيل",
              "True RTL layouts, Arabic-aware search and matching,", "dialect support and Arabic typography from screen one.", "blue"),
             ("test-tube-diagonal", "Tested & honest", "موثوق وصريح",
              "Self-test routes and CI builds, and READMEs that state", "their limits and risks openly instead of hiding them.", "amber")]
    W, gap, th = 1000, 24, 150
    tile = (W - gap) / 2
    H = 2 * th + gap
    d = "".join(grad(f"a{i}", *ACCENTS[acc]) for i, (*_, acc) in enumerate(items))
    d += f'<clipPath id="cp"><rect width="{tile}" height="{th}" rx="22"/></clipPath>'
    b = []
    for i, (icon, en, ar, l1, l2, acc) in enumerate(items):
        x = (i % 2) * (tile + gap)
        y = (i // 2) * (th + gap)
        c1 = ACCENTS[acc][0]
        b.append(f'<g transform="translate({x} {y})"><g clip-path="url(#cp)"><rect width="{tile}" height="{th}" fill="{PANEL}"/>'
                 f'<circle cx="{tile - 20}" cy="10" r="100" fill="{c1}" opacity=".09"/></g>'
                 f'<rect x=".5" y=".5" width="{tile - 1}" height="{th - 1}" rx="22" fill="none" stroke="{EDGE}"/>'
                 f'<rect x="24" y="26" width="58" height="58" rx="18" fill="url(#a{i})"/>{lu(icon, 38, 40, 30, "#FFFFFF")}'
                 f'{text(100, 52, en, 21, INK, 800)}{text(100, 78, ar, 16, c1, 700, family=ARF)}'
                 f'{text(24, 112, l1, 13.5, "#B7C6EA")}{text(24, 132, l2, 13.5, "#B7C6EA")}</g>')
    write("principles.svg", svg(W, H, "".join(b), d, "", "Principles"))


# ───────────────────────── footer ─────────────────────────
def build_footer():
    W, H = 1000, 120
    d = grad("f", "#0E1630", "#0A1024", 0, 0, 0, 1)
    b = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="url(#f)" stroke="{EDGE}"/>'
         '<g transform="translate(420 22)"><rect width="160" height="12" fill="#0B0B0B"/><rect y="12" width="160" height="12" fill="#F4F4F4"/>'
         '<rect y="24" width="160" height="12" fill="#0F9D58"/><path d="M0 0 L52 18 L0 36 Z" fill="#E4312B"/></g>'
         + text(W / 2, 84, "Crafted with love from Palestine · Gaza", 17, INK, 700, "middle")
         + text(W / 2, 108, "صُنع بكل حب من فلسطين · غزة", 15, MUTED, 600, "middle", ARF))
    write("footer.svg", svg(W, H, b, d, "", "Crafted with love from Palestine"))


def main():
    OUT.mkdir(exist_ok=True)
    build_banner()
    build_nav()
    build_contact()
    build_headers()
    build_stats()
    build_cards()
    build_stack()
    build_principles()
    build_footer()
    print("assets generated:", sum(1 for _ in OUT.rglob("*.svg")))


if __name__ == "__main__":
    main()
