import datetime

"""
Reads in raw content and returns:
    title - article title
    summary - cut & interlinked summary block
    full - entire standalone page
"""

def draft(content, pageid):
    title, summary, full = "", "", ""
    cutoff, header = False, True

    form_date = datetime.datetime.now().strftime("%b&nbsp;%-d&nbsp;%Y<br>%-I:%M&nbsp;%p")

    for line in content:
        if "<!--" in line:
            header = True

        if header:
            if "-->" in line:
                header = False

            ls = line.strip()

            if ls.startswith(":title "):
                title = ls[7:]

            elif ls.startswith(":date "):
                form_date = ls[6:]

            # IMPLEMENT TAGS HERE LATER

        if not cutoff and "[[ENDSUM]]" in line:
            summary += line.split("[[ENDSUM]]")[0] + "...\n"
            cutoff = True

        elif not cutoff:
            summary += line

        full += line

    pubname = title.lower().replace(' ', '-')
    if len(pubname) > 32: pubname = pubname[:32]
    pubname = str(pageid) + '_' + pubname

    summary = f"""<div class="post"><div class="content">
<div class="post-title">
    <a class="post-title-name" href="posts/{pubname}">{title}</a>
    <div class="post-title-date">{form_date}</div>
</div>\n""" + summary
    if cutoff:
        summary += f"""<p><a class="readmore" href="{pubname}">read more</a></p>\n"""
    summary += "</div></div>"

    full = f"""<div class="post"><div class="content">
<div class="post-title">
    <a class="post-title-name" href="{pubname}">{title}</a>
    <div class="post-title-date">{form_date}</div>
</div>\n""" + full
    full += "</div></div>"

    return (title, summary, full)
