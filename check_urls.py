import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.urls import get_resolver, reverse, NoReverseMatch  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))

resolver = get_resolver()


def all_names(res, prefix=""):
    out = set()
    for pattern in res.url_patterns:
        if hasattr(pattern, "url_patterns"):
            out |= all_names(pattern, prefix)
        else:
            try:
                out.add(pattern.name)
            except AttributeError:
                pass
    return out


names = all_names(resolver)
print("Registered URL names:", sorted(n for n in names if n))

problems = []
for root, _, files in os.walk(os.path.join(BASE, "templates")):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        fp = os.path.join(root, fn)
        src = open(fp, encoding="utf-8").read()
        for m in re.finditer(r"{%\s*url\s+['\"]([\w:-]+)['\"]", src):
            nm = m.group(1)
            if nm not in names:
                problems.append(f"MISSING URL: {fp} -> {nm!r}")

if problems:
    print("\nISSUES FOUND:", len(problems))
    for p in sorted(set(problems)):
        print(" -", p)
else:
    print("\nALL TEMPLATE URL REFERENCES OK")
