from source.files import *
import os

starship_version = 1.3

def collect(body, index, styleroot):
    final = ""

    template = open("source/template.html")
    page_title = readfrom("../name.txt").strip()

    for line in template:
        final += line

        if line.startswith("<!--"):
            if "head" in line:
                final += readfrom("source/head.html")

            elif "css" in line:
                final += f"<link rel=\"stylesheet\" href=\"{styleroot}\">"

            elif "title" in line:
                final += f"<title>{page_title}</title>\n"

            elif "grabber" in line:
                final += f"<div id=\"starship\">Powered by Starship v{starship_version}<div id=\"grabber\">🔥</div></div>\n"

            elif "name" in line:
                final += f"<a href=\"{index}\">{page_title}</a>\n"

            elif "posts" in line:
                final += body

    template.close()

    return final
