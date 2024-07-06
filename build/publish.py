from source.collect import collect
from source.draft import draft
from source.files import *

from source.chunk import chunk

import sys
import os

if os.path.dirname(os.path.realpath(__file__)) != os.getcwd():
    print("Please run `publish.py` from build dir!")
    exit()

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
    if not os.path.exists("../pages/"):
        os.mkdir("../pages/")
        writeto("../pages/state", "0")
    pid = int(readfrom("../pages/state")) + 1

    draft_f = None

    # parse draft
    try:
        draft_f = draft(readfrom(page), pid)
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

    try:
        if not "hidden" in draft_f[0]:
            if not os.path.exists("../content/"):
                os.mkdir("../content/")
            if not os.path.exists("../content/main/"):
                os.mkdir("../content/main/")
                writeto("../content/main/state", "0")
                writeto("../content/main/chunk", "0")
            chunk(draft_f[1], "../content/main/")

        for tag in draft_f[0]:
            if tag != "hidden":
                if not os.path.exists(f"../content/{tag}/"):
                    os.mkdir(f"../content/{tag}/")
                    writeto(f"../content/{tag}/state", "0")
                    writeto(f"../content/{tag}/chunk", "0")
                chunk(draft_f[1], f"../content/{tag}/", gentag(tag))
        
        standalone = collect(draft_f[2], "../content/main/index.html", "../style.css")
        writeto(f"../pages/{draft_f[3]}.html", standalone)

        writeto("../pages/state", str(pid))

        if not os.path.exists("artifacts/"):
            os.mkdir("artifacts/")
            writeto("artifacts/state", "")

        appendto("artifacts/state", draft_f[3] + '\n')
        writeto(f"artifacts/{draft_f[3]}.html", draft_f[4])
    except Exception as e:
        print(e)
        return

    # delete draft
    try:
        os.remove(page)
    except Exception as e:
        print(e)
        return

    print("Index updated successfully")

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-y": continue
    print(f"\nHandling {sys.argv[i]}")
    handle(sys.argv[i])
