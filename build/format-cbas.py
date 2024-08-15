code = ''

while True:
    try:
        line = input()
        code += line + '\n'

    except: break

code = code.replace('\t', '    ').split('\n')

tokens = ['']
splits = [
        ' ', ';', ':', '=', '<', '>', '~', '!', '&', '|', '^',
        '.', '-', '*', '/', '+', '%', '?', '(', ')', '[', ']',
        ',', '{', '}'
    ]

for line in code:
    if line.strip().startswith('//'):
        if len(tokens[-1]): tokens.append(line)
        else: tokens[-1] = line

    elif line.strip().startswith('/*') and line.strip().endswith('*/'):
        if len(tokens[-1]): tokens.append(line)
        else: tokens[-1] = line

    elif line.strip().startswith('#include'):
        if len(tokens[-1]): tokens.append('#include')
        else: tokens[-1] = '#include'
        tokens.append(' ')
        tokens.append(line.strip()[9:])

    elif len(line.strip()):
        if len(tokens[-1]): tokens.append('')

        instring, escape = False, False

        for c in line:
            if instring:
                if c == instring and not escape:
                    tokens[-1] += c
                    tokens.append('')
                    instring = False

                else:
                    tokens[-1] += c

                    if c == '\\': escape = True
                    else: escape = False

            elif c in ['"', "'"]:
                instring = c
                if len(tokens[-1]): tokens.append(c)
                else: tokens[-1] = c

            elif c in splits:
                if len(tokens[-1]): tokens.append(c)
                else: tokens[-1] = c
                tokens.append('')

            else: tokens[-1] += c

    if len(tokens[-1]): tokens.append('\n')
    else: tokens[-1] = '\n'

if not len(tokens[-1]): tokens.pop()
while len(tokens) and tokens[-1] == '\n': tokens.pop()

escape = [['&', '&amp;'], ['<', '&lt;'], ['>', '&gt;']]

for i in range(len(tokens)):
    for e in escape:
        tokens[i] = tokens[i].replace(e[0], e[1])

    if i and tokens[i] == '\n' and tokens[i-1] in ['\n', '<br>']:
        tokens[i-1] = '<br>'

types = [
        'uint', 'int', 'float', 'double', 'char', 'void', 'byte', 'u8', 'string',
        'u16', 'u32', 'u64', 'i8', 'i16', 'i32', 'i64', 'bool', 'll', 'ull',
        'codegen', 'predecl', 'atomic', 'noexport', 'static', 'inline', 'pure', 'pub'
    ]

control = [
        'struct', 'union', 'enum', 'class', 'data',
        'fn', 'method', 'break', 'continue', 'return', 'goto', 'scope',
        'tail', 'for', 'while', 'if', 'else', 'elif', 'end', 'switch'
        'sizeof', 'malloc', 'free', 'cast', 'realloc', 'asm'
    ]

reserved = {
        'ln': 'b', 'sp': 'b', 'fl': 'b'
    }

for t in types: reserved[t] = 'g'
for s in control: reserved[s] = 'y'

out = ''

def iscom(i):
    return i.strip().startswith('//') or (i.strip().startswith('/*') and i.strip().endswith('*/'))

def isnum(i):
    if tokens[i] == '-':
        if i == len(tokens)-1: return False
        return isonly(tokens[i+1], '0123456789e')

    if tokens[i] in '.':
        if i == len(tokens)-1 or i == 0: return False
        return isonly(tokens[i-1], '0123456789e') and isonly(tokens[i+1], '0123456789e')

    if len(tokens[i]) > 1 and tokens[i][0] == '0' and tokens[i][1] == 'x':
        return isonly(tokens[i][2:], '0123456789abcdef')

    return isonly(tokens[i], '0123456789e')

def isstr(i):
    return len(i) > 2 and i[0] in ["'", '"'] and i[-1] == i[0]

def isonly(s, allowed):
    val = 0
    for c in s:
        if c in allowed: val += 1
    return val == len(s)

def isparsehook(i):
    return tokens[i].startswith('@')

def isdef(i):
    return i > 1 and tokens[i-1] == ' ' and tokens[i-2] in ['#define', '#ifdef', '#ifndef', '#guard']

def isinc(i):
    if tokens[i].startswith('&lt;') and tokens[i].endswith('&gt;'): return True
    return tokens[i][0] == '"' and tokens[i][len(tokens[i])-1] == '"' and i > 1 and tokens[i-1] == ' ' and tokens[i-2] == '#include'

def isop(i):
    return i in ';:=~!&|^.-*/+%?' or i in ['&lt;', '&gt;', 'streq', 'strneq']

for i in range(len(tokens)):
    if tokens[i] in reserved:
        out += f'<span class={reserved[tokens[i]]}>{tokens[i]}</span>'

    else:
        if iscom(tokens[i]):
            out += f'<span class=r>{tokens[i]}</span>'

        elif isdef(i) or isinc(i) or isparsehook(i):
            out += f'<span class=b>{tokens[i]}</span>'

        elif isnum(i) or isstr(tokens[i]):
            out += f'<span class=y>{tokens[i]}</span>'

        elif tokens[i].startswith('#'):
            out += f'<span class=y>{tokens[i]}</span>'
        
        elif isop(tokens[i]):
            out += f'<span class=b>{tokens[i]}</span>'

        else: out += tokens[i]

print(out)
