from source.collect import collect
from source.draft import draft as Draft

import sys
import os

# sanity checks
if len(sys.argv) == 1:
    print("Usage: `publish.py <draft.html>`")
    exit()

defer = "-y" in sys.argv

def handle(page):
    if not page.endswith(".html"):
        print("Draft must be .html")
        return

    # obtain new page id
    pid = int(open(".artifacts/state").read().strip()) + 1

    draft = None

    # parse draft
    try:
        reader = open(page)
        draft = Draft(reader, pid)
        reader.close()
    except Exception as e:
        print(e)
        return

    def conf(p):
        if defer: return
        while True:
            i = input(f"{p} (y/N): ")
            if len(i) == 0: return 1
            if i in "yY": return 0
            if i in "nN": return 1

    if conf("Are your artifacts synced?"): return

    # extend artifact & update
    try:
        content = draft[1] + "\n<div class=\"post-spacer\"></div>\n"
        artifact = open(".artifacts/index.html")
        content += artifact.read()
        artifact.close()

        final = collect(content, "index.html", "style.css")

        if conf("You are updating main. Proceed?"): return

        artifact = open(".artifacts/index.html", "w")
        artifact.write(content)
        artifact.close()

        index = open("../index.html", "w")
        index.write(final)
        index.close()

        standalone = collect(draft[2], "../index.html", "../style.css")
        post = open(f"../pages/{draft[3]}.html", "w")
        post.write(standalone)
        post.close()

        state = open(".artifacts/state", "w")
        state.write(str(pid))
        state.close()

        state = open(".artifacts/part/state", "a")
        state.write(draft[3] + ".html\n")
        state.close()

        artifact = open(f".artifacts/part/{draft[3]}.html", "w")
        artifact.write(draft[1])
        artifact.close()
    except Exception as e:
        print(e)
        return

    # try delete file
    try:
        if not conf("Delete draft?"):
            os.remove(page)
    except Exception as e:
        print(e)
        return

    print("Index updated successfully")

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-y": continue
    print(f"\nHandling {sys.argv[i]}")
    handle(sys.argv[i])
