print("Starship Quick Setup\n")

title = input("Enter blog title (can be changed later): ")

f = open("build/source/title.cfg")
f.write(title)
f.close()
