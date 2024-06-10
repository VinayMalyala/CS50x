from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

for i in range(1, height+1):
    for j in range(1, height-i+1):
        print(" ", end="")
    for k in range(1, i+1):
        print("#", end="")
    print("  ", end="")
    for a in range(1, i+1):
        print("#", end="")
    print()
