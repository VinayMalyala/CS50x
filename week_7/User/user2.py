import csv

with open("user.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["First name"],row["Last name"])
