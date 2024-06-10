from cs50 import get_int

x = get_int("Whats's x? ")
y = get_int("Whats's y? ")

if x<y:
    print("x is less than y")
elif x>y:
    print("x is greater than y")
else:
    print("x is equal to y")
