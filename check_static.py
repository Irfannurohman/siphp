import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT_DIR = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None

problems = []
checked = 0
for root, _, files in os.walk(os.path.join(BASE, "templates")):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(root, fn)
        src = open(fp, encoding="utf-8").read()

        # {% static 'path' %}
        for m in re.finditer(r"{%\s*static\s+['\"]([^'\"]+)['\"]", src):
            rel = m.group(1)
            checked += 1
            if STATIC_ROOT_DIR:
                abs_p = os.path.join(STATIC_ROOT_DIR, rel.replace("/", os.sep))
                if not os.path.exists(abs_p):
                    problems.append(f"MISSING STATIC: {fp} -> {rel!r}")

        # src="/static/..." dan href="/static/..."
        for m in re.finditer(r"(?:src|href)=[\"']/static/([^\"']+)[\"']", src):
            rel = m.group(1)
            checked += 1
            if STATIC_ROOT_DIR:
                abs_p = os.path.join(STATIC_ROOT_DIR, rel.replace("/", os.sep))
                if not os.path.exists(abs_p):
                    problems.append(f"MISSING STATIC(literal): {fp} -> {rel!r}")

print(f"Checked {checked} static references")
if problems:
    print("ISSUES FOUND:", len(problems))
    for p in sorted(set(problems)):
        print(" -", p)
else:
    print("ALL STATIC REFERENCES OK")
