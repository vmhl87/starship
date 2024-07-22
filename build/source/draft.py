import datetime

"""
Reads in raw content and returns:
    tags - article tags, deduplicated
    summary - cut & interlinked summary block
    full - entire standalone page
    pubname - pagename in URL
    repacked - repacked draft with timestamp
"""

def draft(content, pageid):
    title, summary, full, re_head, re_tail = "", "", "", "", ""
    cutoff, header, had_header, re_swap, re_date = False, False, False, False, False

    tags = []

    form_date = datetime.datetime.now().strftime("%b&nbsp;%-d&nbsp;%Y<br>%-I:%M&nbsp;%p")

    for ln in content.split('\n'):
        line = ln + '\n'

        if len(line.strip()) == 0: continue

        if re_swap: re_tail += line
        else: re_head += line

        if "<!--" in line and not had_header:
            had_header = True
            header = True

        if header:
            if "-->" in line:
                header = False

            ls = line.strip()

            if ls.startswith(":title "):
                title = ls[7:]
                re_swap = True

            elif ls.startswith(":date "):
                form_date = ls[6:].replace(' ', '&nbsp;')
                re_date = True

            elif ls.startswith(":tag "):
                for tag in ls[5:].split(' '):
                    if tag not in tags:
                        tags.append(tag)

            continue

        if not cutoff and "[[ENDSUM]]" in line:
            summary += line.split("[[ENDSUM]]")[0] + "...\n"
            full += line.replace("[[ENDSUM]]", "")
            cutoff = True

        elif not cutoff:
            summary += line
            full += line

        else: full += line

    if not had_header:
        raise Exception("Draft does not have a header")

    if len(title) == 0:
        raise Exception("Draft does not have a title")

    if not re_date:
        re_head += f'\t:date {datetime.datetime.now().strftime("%b %-d %Y<br>%-I:%M %p")}\n'

    while "main" in tags:
        tags.remove("main")

    pubname = ""
    for x in title.lower():
        if x == ' ' or (ord(x) >= ord('a') and ord(x) <= ord('z')):
            pubname += x
    pubname = pubname.replace(' ', '-')
    if len(pubname) > 16: pubname = pubname[:16]
    pubname = str(pageid) + '_' + pubname

    summary = f"""<div class="post"><div class="content">
<div class="post-title">
    <a class="post-title-name" href="../../pages/{pubname}.html">{title}</a>
    <div class="post-title-date">{form_date}</div>
</div>\n""" + summary
    if cutoff:
        summary += f"""<p><a class="readmore" href="../../pages/{pubname}.html">read more</a></p>\n"""

    full = f"""<div class="post"><div class="content">
<div class="post-title">
    <a class="post-title-name" href="{pubname}.html">{title}</a>
    <div class="post-title-date">{form_date}</div>
</div>\n""" + full

    if len(tags) != 0:
        summary += "<p class=\"tag-container\">tags: "
        full += "<p class=\"tag-container\">tags: "
        for tag in tags:
            summary += f"<a href=\"../{tag}/index.html\">{tag}</a> "
            full += f"<a href=\"../content/{tag}/index.html\">{tag}</a> "
        summary += "</p>"
        full += "</p>"

    summary += "</div></div>"
    full += "</div></div>"

    return (tags, summary, full, pubname, re_head+re_tail)
