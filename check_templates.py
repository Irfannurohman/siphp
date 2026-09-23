import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

problems = []
for root, _, files in os.walk(os.path.join(BASE, "templates")):
    for fn in files:
        if not fn.endswith((".html", ".txt")):
            continue
        fp = os.path.join(root, fn)
        try:
            src = open(fp, encoding="utf-8").read()
        except UnicodeDecodeError:
            problems.append(f"DECODE ERROR: {fp}")
            continue

        open_t = len(re.findall(r"{%", src))
        close_t = len(re.findall(r"%}", src))
        open_v = len(re.findall(r"{{", src))
        close_v = len(re.findall(r"}}", src))
        if open_t != close_t:
            problems.append(f"UNBALANCED %: {fp} open={open_t} close={close_t}")
        if open_v != close_v:
            problems.append(f"UNBALANCED }}: {fp} open={open_v} close={close_v}")

        # block tags harus ada tutupnya
        blocks = re.findall(r"{%\s*block\s+[\w-]+", src)
        endblocks = len(re.findall(r"{%\s*endblock", src))
        if len(blocks) != endblocks:
            problems.append(f"BLOCK MISMATCH: {fp} block={len(blocks)} endblock={endblocks}")

        for m in re.findall(r"{%[ \t]*[A-Za-z]+[^%]*%}", src):
            tag = re.match(r"{%\s*(\w+)", m)
            if not tag:
                problems.append(f"BAD TAG: {fp} -> {m[:60]!r}")

        # {%%} kosong / {{ }}
        if re.search(r"{%\s*%}", src):
            problems.append(f"EMPTY TAG: {fp}")
        if re.search(r"{{\s*}}", src):
            problems.append(f"EMPTY VAR: {fp}")

if problems:
    print("ISSUES FOUND:", len(problems))
    for p in problems:
        print(" -", p)
else:
    print("ALL TEMPLATES OK")
