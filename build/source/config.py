def title():
    return "Blog"

def version():
    f = open("state.txt")
    v = int(f.read().split('\n')[1].split(' ')[0])
    f.close()
    return v

def postcount():
    f = open("state.txt")
    v = int(f.read().split('\n')[0].split(' ')[0])
    f.close()
    return v

def setpostcount(p):
    f = open("state.txt")
    a = f.read().split['\n']
    f.close()
    a[0] = str(p) + " :: pages"
    f = open("state.txt", "w")
    for b in a: f.write(b)
    f.close()
