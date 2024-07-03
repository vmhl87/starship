def readfrom(fname):
    f = open(fname)
    ret = f.read()
    f.close()
    return ret

def writeto(fname, body):
    f = open(fname, "w")
    f.write(body)
    f.close()

def appendto(fname, body):
    f = open(fname, "a")
    f.write(body)
    f.close()

def getspacer():
    return "\n<div class=\"post-spacer\"></div>\n"

def oldsec(sec):
    return f"""<div class="post-spacer"></div>
<div class="oldposts">
    <a id="older-posts" href={sec}.html">Older Posts</a>
</div>
"""
