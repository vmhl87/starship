import datetime

"""
Reads in raw content and returns:
    title - article title
    summary - cut & interlinked summary block
    full - entire standalone page
    pubname - pagename in URL
"""

def draft(content, pageid):
    title, summary, full = "", "", ""
    cutoff, header, had_header = False, False, False

    form_date = datetime.datetime.now().strftime("%b&nbsp;%-d&nbsp;%Y<br>%-I:%M&nbsp;%p")

    for line in content:
        if len(line.strip()) == 0: continue

        if "<!--" in line:
            had_header = True
            header = True

        if header:
            if "-->" in line:
                header = False

            ls = line.strip()

            if ls.startswith(":title "):
                title = ls[7:]

            elif ls.startswith(":date "):
                form_date = ls[6:].replace(' ', '&nbsp;')

            # IMPLEMENT TAGS HERE LATER

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

    pubname = ""
    for x in title.lower():
        if x == ' ' or (ord(x) >= ord('a') and ord(x) <= ord('z')):
            pubname += x
    pubname = pubname.replace(' ', '-')
    if len(pubname) > 16: pubname = pubname[:16]
    pubname = str(pageid) + '_' + pubname

    summary = f"""<div class="post"><div class="content">
<div class="post-title">
    <a class="post-title-name" href="pages/{pubname}.html">{title}</a>
    <div class="post-title-date">{form_date}</div>
</div>\n""" + summary
    if cutoff:
        summary += f"""<p><a class="readmore" href="pages/{pubname}.html">read more</a></p>\n"""
    summary += "</div></div>"

    full = f"""<div class="post"><div class="content">
<div class="post-title">
    <a class="post-title-name" href="{pubname}.html">{title}</a>
    <div class="post-title-date">{form_date}</div>
</div>\n""" + full
    full += "</div></div>"

    return (title, summary, full, pubname)
