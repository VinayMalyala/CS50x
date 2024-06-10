import csv

books = []

# Add books to shelf by reading from books.csv
file = open("books.csv", "r")
reader = csv.DictReader(file)
for row in reader:
    books.append(row)
file.close()

# Print books
for book in books:
    print(book)
