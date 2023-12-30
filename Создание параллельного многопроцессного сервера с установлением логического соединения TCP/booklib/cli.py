import requests

# Function to display the main menu
def display_menu():
    print("Select an option:")
    print("1. Add a book")
    print("2. Delete a book")
    print("3. Sort books")
    print("4. Exit")

# Function to add a book
def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    data = {'title': title, 'author': author}
    r = requests.post('http://localhost:5000/books', json=data)
    if r.status_code == 201:
        print("Book added successfully!")
    else:
        print("Error adding book.")

# Function to delete a book
def delete_book():
    book_id = input("Enter the ID of the book to delete: ")
    r = requests.delete(f'http://localhost:5000/books/{book_id}')
    if r.status_code == 200:
        print("Book deleted successfully!")
    else:
        print("Error deleting book.")

# Function to sort books
def sort_books():
    sort_by = input("Enter the field to sort by (title or author): ")
    r = requests.get(f'http://localhost:5000/books?sort={sort_by}')
    if r.status_code == 200:
        books = r.json()
        for book in books:
            print(f"{book['id']}: {book['title']} by {book['author']}")
    else:
        print("Error getting books.")

# Main loop
while True:
    display_menu()
    choice = input()
    if choice == '1':
        add_book()
    elif choice == '2':
        delete_book()
    elif choice == '3':
        sort_books()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")
