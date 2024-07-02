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
    pid = int(open("../pages/state").read().strip()) + 1

    # current fragment size
    fsz = int(open(".artifacts/state").read().strip()) + 1

    # current oldpage ID
    oid = int(open("../old/state").read().strip())

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
        content = draft[1]
        if pid != 1: content += "\n<div class=\"post-spacer\"></div>\n"
        artifact = open(".artifacts/index.html")
        content += artifact.read()
        artifact.close()

        if conf("You are updating main. Proceed?"): return

        artifact = open(".artifacts/index.html", "w")
        artifact.write(content)
        artifact.close()
 
        if fsz == 40:
            # rotate index, old
            # also do smth with oid
            if os.path.isfile(".artifacts/old.html"):
                oid += 1
                ostr = open("../old/state", "w")
                ostr.write(str(oid))
                ostr.close()

                xfer = open(f"../old/{oid}.html", "w")
                xfer.write(open(".artifacts/old.html").read())
                xfer.close()

            xfer = open(".artifacts/old.html", "w")
            xfer.write(content)
            xfer.close()

            xfer = open(".artifacts/index.html", "w")
            xfer.write("<!-- op 0 -->")
            xfer.close()

            fsz = 0
        
        content = open(".artifacts/index.html").read()

        if os.path.isfile(".artifacts/old.html"):
            content += open(".artifacts/old.html").read()

        if oid > 0:
            content += f"""<div class="post-spacer"></div>
<div style="margin: 0 auto; text-align: center">
    <a id="older-posts" href="old/{oid}.html">Older Posts</a>
</div>
"""
       
        final = collect(content, "index.html", "style.css")

        index = open("../index.html", "w")
        index.write(final)
        index.close()

        standalone = collect(draft[2], "../index.html", "../style.css")
        post = open(f"../pages/{draft[3]}.html", "w")
        post.write(standalone)
        post.close()

        state = open("../pages/state", "w")
        state.write(str(pid))
        state.close()

        state = open(".artifacts/state", "w")
        state.write(str(fsz))
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
