from source.collect import collect
from source.files import *

import os

# Takes in draft as preformatted HTML and location to push.
# Handles new/old/state and advances queue.
# Assumes location is already init.
def chunk(draft, loc, head=""):
    try:
        state = int(readfrom(f"{loc}state")) + 1

        content = draft
        if state != 1: content += getspacer()
        if os.path.exists(f"{loc}new.html"):
            content += readfrom(f"{loc}new.html")

        writeto(f"{loc}new.html", content)

        chunk = int(readfrom(f"{loc}chunk"))
 
        if state == 40:
            # rotate new/old, push old
            if os.path.exists(f"{loc}old.html"):
                chunk += 1
                writeto(f"{loc}chunk", str(chunk))

                nextcont = readfrom(f"{loc}old.html")
                if oid > 1: nextcont += oldsec(oid-1)
                formcont = collect(head + nextcont, "index.html", "../../style.css")

                writeto(f"{loc}{oid}.html", formcont)

            writeto(f"{loc}old.html", readfrom(f"{loc}new.html"))
            writeto(f"{loc}new.html", "")

            state = 0
        
        content = readfrom(f"{loc}new.html")

        if os.path.isfile(f"{loc}old.html"):
            content += getspacer()
            content += readfrom(f"{loc}old.html")

        if chunk > 0: content += oldsec(oid)
       
        final = collect(head + content, "index.html", "../../style.css")

        writeto(f"{loc}index.html", final)

        writeto(f"{loc}state", str(state))

    except Exception as e:
        print(e)
        return
