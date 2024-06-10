def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Not an integer")


def main():
    x = get_int("x: ")
    y = get_int("y: ")

    print(x+y)

main()


'''
x = int(input("x: "))
y = int(input("y: "))

z = x/y
# print(format(z,".5f"))

print(f"{z:.5f}")
'''
