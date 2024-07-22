code = ''

while True:
    try:
        line = input()
        code += line + '\n'

    except: break

code = code.replace('\t', '    ').split('\n')

tokens = ['']
splits = [
        ' ', '*', '&', '[', ']', '(', ')', '{', '}', ';',
        ',', '.', '>', '<', '=', '-', '+', '/', '?', ':'
    ]

for line in code:
    if line.strip().startswith('//'):
        if len(tokens[-1]): tokens.append(line)
        else: tokens[-1] = line

    else:
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

reserved = {
        'struct': 'g', 'union': 'g', 'enum': 'g', 'static': 'g', 'inline': 'g',
        'void': 'g', 'const': 'g', 'constexpr': 'g', 'volatile': 'g', 'static': 'g', 'auto': 'g',
        'int': 'g', 'long': 'g', 'float': 'g', 'double': 'g', 'char': 'g', 'bool': 'g', 'size_t': 'g',
        'unsigned': 'g', 'signed': 'g', 'short': 'g',
        'true': 'y', 'false': 'y', 'null': 'y',
        'malloc': 'y', 'free': 'y', 'assert': 'y', 'using': 'y', 'typedef': 'y',
        'break': 'y', 'continue': 'y', 'return': 'y', 'goto': 'y',
        'while': 'y', 'if': 'y', 'for': 'y', 'do': 'y', 'else': 'y', 'switch': 'y', 'case': 'y',
        '[': 'b', ']': 'b'
    }

out = ''

def iscom(i):
    return i.strip().startswith('//')

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

def islbl(s):
    return len(s) > 1 and s[-1] == ':'

def isstruct(i):
    if tokens[i] == ' ': return False

    if i == 0: return False
    if tokens[i-1] == 'struct': return True

    if tokens[i-1] == ' ':
        if i == 1: return False
        
        return tokens[i-2] == 'struct'

    return False

def isfunc(i):
    if tokens[i] == ' ': return False

    if i == len(tokens)-1: return False
    if tokens[i+1] == '(': return isonly(tokens[i], 'abcdefghijklmnopqrstuvwxyz0123456789')

    if tokens[i+1] == ' ':
        if i == len(tokens)-2: return False
        
        return tokens[i+2] == '(' and isonly(tokens[i], 'abcdefghijklmnopqrstuvwxyz0123456789')
    
    return False

def isdef(i):
    return i > 1 and tokens[i-1] == ' ' and tokens[i-2] == '#define'

def isinc(i):
    if tokens[i] == '&lt;': return i > 1 and tokens[i-1] == ' ' and tokens[i-2] == '#include'
    if tokens[i] == '&gt;': return i > 3 and isinc(i-1)
    return i > 2 and tokens[i-1] == '&lt;' and tokens[i+1] == '&gt;' and isinc(i-1)

for i in range(len(tokens)):
    if tokens[i] in reserved:
        out += f'<span class={reserved[tokens[i]]}>{tokens[i]}</span>'

    else:
        if iscom(tokens[i]):
            out += f'<span class=r>{tokens[i]}</span>'

        elif isnum(i) or islbl(tokens[i]) or isstr(tokens[i]):
            out += f'<span class=y>{tokens[i]}</span>'

        elif tokens[i].startswith('#'):
            out += f'<span class=y>{tokens[i]}</span>'

        elif isstruct(i) or isfunc(i) or isdef(i) or isinc(i):
            out += f'<span class=b>{tokens[i]}</span>'

        else: out += tokens[i]

print(out)
