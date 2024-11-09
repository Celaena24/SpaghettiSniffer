file = open("example.txt", "r")
data = file.read()
file.close()

with open("good_example.txt", "r") as f:
    data = f.read()

