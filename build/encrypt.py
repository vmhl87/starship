import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

#AES ECB mode without IV

def encrypt(raw, k):
    key = k.ljust(16, '0')
    raw = pad(raw.encode(),16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw)).decode("utf-8", "ignore")

def decrypt(enc, k):
    key = k.ljust(32, '0')
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc),16).decode("utf-8", "ignore")

def usage(x=None):
    if x == "preview":
        print("""Usage: encrypt.py preview <draft>
`draft` must be html""")

    elif x == "publish":
        print("""Usage: encrypt.py publish <draft>
`draft` must be html""")

    else:
        print("""Usage: encrypt.py <type> <draft>
`type` can be any of: preview, publish
`draft` must be html""")

import os, sys

if len(sys.argv) == 1:
    usage()

elif len(sys.argv) == 2:
    usage(sys.argv[1])

elif len(sys.argv) != 3:
    print("Too many arguments")

elif not sys.argv[1] in ["preview", "publish"]:
    usage()

elif not sys.argv[2].endswith(".html"):
    print("Invalid file")

else:
    f = open(sys.argv[2])

    inheader, head, tail = True, '', ''

    for line in f:
        if inheader:
            if line == "-->\n":
                inheader = False
            head += line
            
        else:
            tail += line

    f.close()

    key = input("Decryption key: ")

    angle = False
    block, ciph = '', ''
    blen, light = 0, 1

    for c in tail.strip():
        if angle:
            if c == '>':
                angle = False

            ciph += c

        else:
            if c == '<':
                angle = True

                if blen:
                    ciph += encrypt(block, key)
                    block = ''
                    blen = 0
                    light = 1

                ciph += c

            elif c in " \t\n" and light:
                ciph += c

            else:
                block += c
                blen += 1
                light = 0
    
    w = open("/tmp/ench.html", "w")

    w.write(head)

    if sys.argv[1] == "preview":
        w.write(open("source/decrypt-prev.html").read())

    else:
        w.write(open("source/decrypt.html").read())

    w.write(ciph)

    w.write("</div></div>\n")

    w.close()

    if sys.argv[1] == "preview":
        os.system(f"python3 preview.py /tmp/ench.html")

    else:
        os.system(f"python3 publish.py /tmp/ench.html")
        os.remove(sys.argv[2])
