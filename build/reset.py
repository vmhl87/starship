f = open(".artifacts/index.html", "w")
f.close()

f = open(".artifacts/state", "w")
f.write('0')
f.close()

import os
os.system("rm -f ../pages/*.html")
os.system("rm -f .artifacts/part/*.html")

f = open(".artifacts/part/state", "w")
f.close()
