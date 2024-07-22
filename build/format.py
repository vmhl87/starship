code = ''

while True:
    try:
        line = input()
        code += line + '\n'

    except: break

code = code.replace('\t', '    ').split('\n')

tokens = ['']
splits = [' ', '*', '&', '[', ']', '(', ')', '{', '}', ';', ',', '.', '>', '<', '=', '-', '+', '/']

for line in code:
    if line.strip().startswith('//'):
        if len(tokens[-1]): tokens.append(f'<span class=r>{line}</span>')
        else: tokens[-1] = f'<span class=r>{line}</span>'

    else:
        if len(tokens[-1]): tokens.append('')

        for c in line:
            if c in splits:
                if len(tokens[-1]): tokens.append(c)
                else: tokens[-1] = c
                tokens.append('')

            else: tokens[-1] += c

    if len(tokens[-1]): tokens.append('\n')
    else: tokens[-1] = '\n'

if not len(tokens[-1]): tokens.pop()
while len(tokens) and tokens[-1] == '\n': tokens.pop()

reserved = {
        'struct': 'g', 'union': 'g', 'enum': 'g', 'static': 'g', 'inline': 'g',
        'void': 'g', 'const': 'g', 'constexpr': 'g', 'volatile': 'g', 'static': 'g', 'auto': 'g',
        'int': 'g', 'long': 'g', 'float': 'g', 'double': 'g', 'char': 'g', 'bool': 'g', 'size_t': 'g',
        'unsigned': 'g', 'signed': 'g', 'short': 'g',
        'true': 'y', 'false': 'y', 'null': 'y',
        'malloc': 'y', 'free': 'y', 'assert': 'y', 'using': 'y', 'typedef': 'y',
        'break': 'y', 'continue': 'y', 'return': 'y', 'goto': 'y',
        'while': 'y', 'if': 'y', 'for': 'y', 'do': 'y', 'else': 'y',
        '[': 'b', ']': 'b'
    }

out = ''

def isnum(i):
    if tokens[i] == '-':
        if i == len(tokens)-1: return False
        return isdig(tokens[i+1])

    if tokens[i] in '.':
        if i == len(tokens)-1 or i == 0: return False
        return isdig(tokens[i-1]) and isdig(tokens[i+1])

    if len(tokens[i]) > 1 and tokens[i][0] == '0' and tokens[i][1] == 'x':
        return isonly(tokens[i][2:], '0123456789abcdef')

    return isonly(tokens[i], '0123456789e')

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
    if tokens[i+1] == '(': return True

    if tokens[i+1] == ' ':
        if i == len(tokens)-2: return False
        
        return tokens[i+2] == '('
    
    return False

def isdef(i):
    return i > 1 and tokens[i-1] == ' ' and tokens[i-2] == '#define'

def isinc(i):
    if tokens[i] == '<': return i > 1 and tokens[i-1] == ' ' and tokens[i-2] == '#include'
    if tokens[i] == '>': return i > 3 and isinc(i-1)
    return i > 2 and tokens[i-1] == '<' and tokens[i+1] == '>' and isinc(i-1)

for i in range(len(tokens)):
    if tokens[i] in reserved:
        out += f'<span class={reserved[tokens[i]]}>{tokens[i]}</span>'

    else:
        if isnum(i) or islbl(tokens[i]):
            out += f'<span class=y>{tokens[i]}</span>'

        elif tokens[i].startswith('#'):
            out += f'<span class=y>{tokens[i]}</span>'

        elif isstruct(i) or isfunc(i) or isdef(i) or isinc(i):
            out += f'<span class=b>{tokens[i]}</span>'

        else: out += tokens[i]

print(out)
