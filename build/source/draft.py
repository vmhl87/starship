import datetime

"""
Reads in raw content and returns:
    title - article title
    summary - cut & interlinked summary block
    full - entire standalone page
"""

def draft(content, pubname):
    title, summary, full = "", "", ""
    cutoff, header = False, True

    for line in content:
        if "<!--" in line:
            header = True

        if header:
            if "-->" in line:
                header = False

            ls = line.strip()
            if ls.startswith("<title>") and ls.endswith("</title>"):
                title = ls[7:-8]
            # IMPLEMENT TAGS HERE LATER

        if not cutoff and "[[ENDSUM]]" in line:
            summary += line.split("[[ENDSUM]]")[0] + "...\n"
            cutoff = True

        elif not cutoff:
            summary += line

        full += line

    form_date = datetime.datetime.now().strftime("%b&nbsp;%-d&nbsp;%Y<br>%-I:%M&nbsp;%p")

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
