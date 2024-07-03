print("Starship Quick Setup\n")

title = input("Enter blog title (can be changed later): ")

f = open("build/source/title.cfg", "w")
f.write(title)
f.close()
