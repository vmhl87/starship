import os

cfg_title = "Blog"

cfg_version = 1  # DO NOT CHANGE

def collect(body, pageroot="index.html", styleroot="style.css"):
    final = ""

    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, "template.html")
    template = open(filepath)

    for line in template:
        final += line

        if line.startswith("<!--"):
            if "head" in line:
                filepath = os.path.join(script_dir, "head.html")
                head = open(filepath)
                final += head.read()
                head.close()

            elif "css" in line:
                final += f"<link rel=\"stylesheet\" href=\"{styleroot}\">"

            elif "title" in line:
                title = cfg_title
                final += f"<title>{title}</title>\n"

            elif "grabber" in line:
                version = cfg_version
                final += f"<div id=\"starship\">Powered by Starship v{version}<div id=\"grabber\">🔥</div></div>\n"

            elif "name" in line:
                title = cfg_title
                final += f"<a href=\"{pageroot}\">{title}</a>\n"

            elif "posts" in line:
                final += body

    template.close()

    return final
