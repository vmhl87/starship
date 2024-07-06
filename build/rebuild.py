from source.collect import collect
from source.draft import draft
from source.files import *

from source.chunk import chunk

import shutil
import sys
import os

if os.path.dirname(os.path.realpath(__file__)) != os.getcwd():
    print("Please run `rebuild.py` from build dir!")
    exit()

# I recognize that this is indeed mostly identical to
# the handle() method of publish and it might be good to
# unify the two; I will consider this later.
def handle(page):
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
                if not os.path.exists("../content/"):
                    os.mkdir("../content/")
                if not os.path.exists(f"../content/{tag}/"):
                    os.mkdir(f"../content/{tag}/")
                    writeto(f"../content/{tag}/state", "0")
                    writeto(f"../content/{tag}/chunk", "0")
                chunk(draft_f[1], f"../content/{tag}/", gentag(tag))
        
        standalone = collect(draft_f[2], "../content/main/index.html", "../style.css")
        writeto(f"../pages/{draft_f[3]}.html", standalone)

        writeto("../pages/state", str(pid))
    except Exception as e:
        print(e)
        return

defer = "-y" in sys.argv

def conf(p):
    if defer: return
    while True:
        i = input(f"{p} (y/N): ")
        if len(i) == 0: return 1
        if i in "yY": return 0
        if i in "nN": return 1

if conf("Are your artifacts synced?"): exit()

# remove all dynamic content
if os.path.isdir("../pages/"):
    shutil.rmtree("../pages/")
if os.path.isdir("../content/"):
    shutil.rmtree("../content/")

# add back from repacked
artlist = open("artifacts/state")

for art in artlist:
    handle(f"artifacts/{art.strip()}.html")
    print(f"Handling {art.strip()}... done")

artlist.close()
