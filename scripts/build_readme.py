#!/usr/bin/env python3
"""Builds README.md (English + Arabic sections) from the project data in build_assets.py.
Run after build_assets.py: python3 scripts/build_readme.py"""
import pathlib

import build_assets as A

ROOT = pathlib.Path(__file__).resolve().parent.parent
USER = "https://github.com/Dev-saged"

CONTACT_LINKS = [("instagram", "Instagram @sajedd.0", "https://instagram.com/sajedd.0"),
                 ("facebook", "Facebook saged.t", "https://facebook.com/saged.t"),
                 ("whatsapp", "WhatsApp", "https://wa.me/972597857250"),
                 ("x", "X @saged_al", "https://x.com/saged_al"),
                 ("github", "GitHub @Dev-saged", USER)]

TEXT = {
    "en": dict(hero_alt="Sajed Al-Abadlah — Software Architect from Gaza, Palestine",
               about_alt="I'm Sajed, a software architect from Gaza, Palestine. I design, code and ship complete systems entirely from a mobile phone. "
                         "My work: Arabic-first AI and automation, offline-first systems for the field, and mobile-native delivery.",
               stats_alt="12 featured projects, 6 offline-first systems, Arabic and English interfaces, built on a phone",
               h_alt={"about": "About", "projects": "Featured Projects", "stack": "Tech Stack", "principles": "How I Build",
                      "contact": "Let's Talk", "metrics": "GitHub Metrics"},
               sub_alt={"ai": "AI and Automation", "offline": "Offline-first Systems", "repos": "More Repositories and Experiments",
                        "closed": "Closed-source Tools"},
               nav_alt={"projects": "Projects", "stack": "Stack", "principles": "Principles", "contact": "Contact"},
               demo_alt="Live demo: GRCS on GitHub Pages",
               stack_alt="JavaScript, TypeScript, Python, Kotlin, HTML5, CSS, React, Vite, Tailwind, Flask, Node.js, Express, Gemini, Claude, "
                         "Telegram, GitHub API, Android, PWA, Firebase, Cloudflare, GitHub Actions, FFmpeg, SQLite, PostgreSQL, Temporal, Docker",
               principles_alt="Offline-first, private by design, Arabic-native, tested and honest",
               footer_alt="Crafted with love from Palestine · Gaza", switch_alt="العربية — اقرأ بالعربية", switch="ar"),
    "ar": dict(hero_alt="ساجد العبادلة — مهندس برمجيات من غزة، فلسطين",
               about_alt="أنا ساجد، مهندس برمجيات من غزة، فلسطين. أصمّم وأبرمج وأطلق أنظمة متكاملة بالكامل من الجوال بدون حاسوب. "
                         "عملي يجمع الذكاء الاصطناعي والأتمتة بالعربية أولاً، وأنظمة ميدانية تعمل بلا إنترنت، وتسليم من الجوال وإليه.",
               stats_alt="12 مشروعاً مميزاً، 6 أنظمة تعمل بلا إنترنت، واجهات ثنائية اللغة، مبنية من الجوال",
               h_alt={"about": "نبذة", "projects": "أبرز المشاريع", "stack": "التقنيات", "principles": "فلسفة العمل",
                      "contact": "تواصل معي", "metrics": "إحصائيات"},
               sub_alt={"ai": "الذكاء والأتمتة", "offline": "أنظمة تعمل بلا إنترنت", "repos": "مستودعات وتجارب أخرى",
                        "closed": "أدوات غير منشورة"},
               nav_alt={"projects": "المشاريع", "stack": "التقنيات", "principles": "المبادئ", "contact": "تواصل"},
               demo_alt="تجربة مباشرة: نظام GRCS على GitHub Pages",
               stack_alt="التقنيات المستخدمة: JavaScript وTypeScript وPython وKotlin وReact وFlask وGemini وClaude وAndroid وPWA وFirebase وCloudflare وغيرها",
               principles_alt="تعمل بلا إنترنت، الخصوصية أولاً، عربي أصيل، موثوق وصريح",
               footer_alt="صُنع بكل حب من فلسطين · غزة", switch_alt="English — Read in English", switch="en"),
}


def img(src, alt, extra):
    return f'<img src="assets/{src}" alt="{alt}" {extra}>'


def link(href, inner):
    return f'<a href="{href}">{inner}</a>'


def cards(lang, items):
    out = ['<div align="center">', ""]
    for slug, title, ar, repo, *_rest in items:
        desc = _rest[3 if lang == "en" else 4]
        out.append(link(f"{USER}/{repo}", img(f"{lang}/cards/{slug}.svg", f"{title} — {desc}", 'width="49%"')))
    out += ["", "</div>"]
    return "\n".join(out)


def minis(lang, refs, linked):
    out = ['<div align="center">', ""]
    for slug, title, repo, acc, icon, d_en, d_ar in A.MINI:
        if (repo is not None) != linked:
            continue
        tag = img(f"{lang}/mini/{slug}.svg", f"{title} — {d_en if lang == 'en' else d_ar}", 'width="49%"')
        out.append(link(f"{USER}/{repo}", tag) if repo else tag)
    out += ["", "</div>"]
    return "\n".join(out)


def contact_row(lang):
    rows = []
    for slug, alt, href in (reversed(CONTACT_LINKS) if lang == "ar" else CONTACT_LINKS):
        name = f"contact-{slug}-ar.svg" if lang == "ar" and slug == "whatsapp" else f"contact-{slug}.svg"
        rows.append(link(href, img(name, alt, 'height="52"')))
    return "\n".join(rows)


def section(lang):
    t = TEXT[lang]
    L = lang
    P = A.PROJECTS
    ai, offline = P[:6], P[6:]
    parts = [f'<a id="{L}"></a>', "", '<div align="center">', ""]
    parts += [link(f"#{L}-{slug}", img(f"{L}/nav-{slug}.svg", t["nav_alt"][slug], 'height="40"')) for slug in (("contact", "principles", "stack", "projects") if L == "ar" else ("projects", "stack", "principles", "contact"))]
    parts += ["", "<br><br>", "", contact_row(L), "", "</div>", "", "<br>", ""]
    parts += [f'<a id="{L}-about"></a>', img(f"{L}/h-about.svg", t["h_alt"]["about"], 'width="100%"'), "", "<br><br>", "",
              img(f"{L}/about.svg", t["about_alt"], 'width="100%"'), "", "<br><br>", "",
              img(f"{L}/stats.svg", t["stats_alt"], 'width="100%"'), "", "<br><br>", ""]
    parts += [f'<a id="{L}-projects"></a>', img(f"{L}/h-projects.svg", t["h_alt"]["projects"], 'width="100%"'), "", "<br><br>", ""]
    parts += [img(f"{L}/sub-ai.svg", t["sub_alt"]["ai"], 'width="100%"'), "", "<br>", "", cards(L, ai), "", "<br>", ""]
    parts += [img(f"{L}/sub-offline.svg", t["sub_alt"]["offline"], 'width="100%"'), "", "<br>", "", cards(L, offline), "", '<div align="center">', "",
              link("https://dev-saged.github.io/wasla-system/", img(f"{L}/live-demo.svg", t["demo_alt"], 'height="60"')), "", "</div>", "", "<br>", ""]
    parts += [img(f"{L}/sub-repos.svg", t["sub_alt"]["repos"], 'width="100%"'), "", "<br>", "", minis(L, None, True), "", "<br>", ""]
    parts += [img(f"{L}/sub-closed.svg", t["sub_alt"]["closed"], 'width="100%"'), "", "<br>", "", minis(L, None, False), "", "<br>", ""]
    parts += [f'<a id="{L}-stack"></a>', img(f"{L}/h-stack.svg", t["h_alt"]["stack"], 'width="100%"'), "", "<br><br>", "",
              img(f"{L}/stack.svg", t["stack_alt"], 'width="100%"'), "", "<br><br>", ""]
    parts += [f'<a id="{L}-principles"></a>', img(f"{L}/h-principles.svg", t["h_alt"]["principles"], 'width="100%"'), "", "<br><br>", "",
              img(f"{L}/principles.svg", t["principles_alt"], 'width="100%"'), "", "<br><br>", ""]
    parts += [f'<a id="{L}-contact"></a>', img(f"{L}/h-contact.svg", t["h_alt"]["contact"], 'width="100%"'), "", "<br><br>", "",
              '<div align="center">', "", contact_row(L), "", "</div>", "", "<br><br>", ""]
    parts += [img(f"{L}/h-metrics.svg", t["h_alt"]["metrics"], 'width="100%"'), "", "<br>", "", '<div align="center">', "",
              '<img src="https://github-readme-stats.vercel.app/api?username=Dev-saged&show_icons=true&theme=tokyonight&hide_border=true&title_color=3B82F6&bg_color=0E1630" height="180" alt="GitHub stats">',
              '<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Dev-saged&layout=compact&theme=tokyonight&hide_border=true&title_color=3B82F6&bg_color=0E1630" height="180" alt="Top languages">',
              "<br>",
              '<img src="https://streak-stats.demolab.com/?user=Dev-saged&theme=tokyonight&hide_border=true&stroke=0000&title_color=3B82F6&background=0E1630" alt="Contribution streak">',
              "", "</div>", "", "<br>", "",
              img(f"{L}/footer.svg", t["footer_alt"], 'width="100%"'), "", "<br>", "",
              '<div align="center">', "", link(f"#{t['switch']}", img(f"lang-{t['switch']}.svg", t["switch_alt"], 'width="46%"')), "", "</div>", ""]
    return "\n".join(parts)


def main():
    top = ['<div align="center">', "", img("banner.svg", TEXT["en"]["hero_alt"], 'width="100%"'), "", "<br><br>", "",
           img("lang-title.svg", "Choose your language · اختر لغتك", 'width="100%"'), "", "<br>", "",
           link("#en", img("lang-en.svg", "English — Read the full profile in English", 'width="46%"')),
           link("#ar", img("lang-ar.svg", "العربية — اقرأ الملف الكامل بالعربية", 'width="46%"')), "", "</div>", "", "<br><br>", ""]
    divider = ["<br>", "", "---", "", "<br>", ""]
    text = "\n".join(top) + section("en") + "\n".join(divider) + section("ar")
    (ROOT / "README.md").write_text(text.rstrip() + "\n", encoding="utf-8")
    print("README.md written:", len(text.splitlines()), "lines")


if __name__ == "__main__":
    main()
