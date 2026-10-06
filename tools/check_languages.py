"""Checks a built site for language mix-ups. Run it before every push.

English pages: no Chinese characters anywhere (text, titles, image descriptions, or metadata)
except the one "中文" link to the Chinese version, and they must use the English share card.
Chinese pages (/zh-tw/): marked as zh-Hant-TW, and must use the Chinese share card.

Usage: python3 tools/check_languages.py [built site folder, default _site]
Exits with an error and lists every problem it finds.
"""
import os
import re
import sys

root = sys.argv[1] if len(sys.argv) > 1 else "_site"
CJK = re.compile(r"[⺀-⿟　-〿぀-ヿ㄀-ㄯ㈀-㋿"
                 r"㐀-䶿一-鿿豈-﫿︰-﹏＀-￯]")
SWITCH = re.compile(r'<a class="lang-switch" href="/zh-tw/[^"]*" hreflang="zh-Hant-TW" lang="zh-Hant-TW">中文</a>')
EN_CARD = 'property="og:image" content="https://adamwhansen.com/assets/img/og-card.png"'
ZH_CARD = 'property="og:image" content="https://adamwhansen.com/assets/img/og-card-zh-tw.png"'

problems, checked = [], 0
for folder, _, files in os.walk(root):
    for name in files:
        path = os.path.join(folder, name)
        rel = os.path.relpath(path, root)
        if not name.endswith((".html", ".xml", ".txt", ".json")):
            continue
        text = open(path, encoding="utf-8").read()
        checked += 1
        if rel.startswith("zh-tw" + os.sep):
            if '<html lang="zh-Hant-TW">' not in text:
                problems.append(f"{rel}: not marked as zh-Hant-TW")
            if ZH_CARD not in text:
                problems.append(f"{rel}: doesn't use the Chinese share card")
            continue
        found = sorted(set(CJK.findall(SWITCH.sub("", text))))
        if found:
            problems.append(f"{rel}: Chinese characters on an English page: {''.join(found)[:40]}")
        if "og-card-zh-tw" in text:
            problems.append(f"{rel}: refers to the Chinese share card")
        if name.endswith(".html"):
            if '<html lang="en-US">' not in text:
                problems.append(f"{rel}: not marked as en-US")
            if EN_CARD not in text:
                problems.append(f"{rel}: doesn't use the English share card")

if checked == 0:
    sys.exit(f"No pages found in {root}. Build the site first.")
for p in problems:
    print("PROBLEM:", p)
print(f"Checked {checked} files: {'no problems' if not problems else str(len(problems)) + ' problem(s)'}.")
sys.exit(1 if problems else 0)
