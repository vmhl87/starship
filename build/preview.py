from source.collect import collect
from source.draft import draft
from source.files import *

import sys
import os

if len(sys.argv) == 1:
    print("Usage: `preview.py <draft.html>`")
    exit()

page = sys.argv[1]

if not page.endswith(".html"):
    print("Draft must be .html")
    exit()

try:
    d = draft(readfrom(page), 0)
except Exception as e:
    print(e)
    exit()

try:
    content = d[1] + getspacer() + d[2]
    final = collect(content, ".preview.html", "../style.css")

    writeto(".preview.html", final)
except Exception as e:
    print(e)
    exit()

print(f"Preview at file://{os.getcwd()}/.preview.html")
