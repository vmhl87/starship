print("Starship Quick Setup")

title = input("Enter blog name (you can change later): ")

f = open("build/source/title.cfg")
f.write(title)
f.close()
