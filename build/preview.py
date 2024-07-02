from source.collect import collect
from source.draft import draft

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
    reader = open(page)
    draft = draft(reader, 0, "../")
    reader.close()
except Exception as e:
    print(e)
    exit()

try:
    content = draft[1] + "\n<div class=\"post-spacer\"></div>\n" + draft[2]
    final = collect(content, "../")

    writer = open(".preview.html", "w")
    writer.write(final)
    writer.close()
except Exception as e:
    print(e)
    exit()

print(f"Preview at file://{os.getcwd()}/.preview.html")
