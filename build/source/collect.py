import config as cfg

def collect(body, root_url="index.html"):
    final = ""

    template = open("template.html")

    for line in template:
        final += line

        if line.startswith("<!--"):
            if "head" in line:
                head = open("head.html")
                final += head.read()
                head.close()

            elif "title" in line:
                title = cfg.title()
                final += f"<title>{title}</title>\n"

            elif "grabber" in line:
                version = cfg.version()
                final += f"<div id=\"starship\">Powered by Starship v{version}<div id=\"grabber\">🔥</div></div>\n"

            elif "name" in line:
                title = cfg.title()
                final += f"<a href=\"{root_url}\">{title}</a>\n"

            elif "posts" in line:
                final += body

    template.close()

    return final
