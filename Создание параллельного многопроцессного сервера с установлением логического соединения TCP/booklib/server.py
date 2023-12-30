from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to create the books table
def create_table():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to insert a book into the database
def insert_book(title, author):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    book_id = c.lastrowid
    conn.commit()
    conn.close()
    return book_id

# Function to delete a book from the database
def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Function to get all books from the database
def get_books(sort_by=None):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    if sort_by == 'title':
        c.execute("SELECT * FROM books ORDER BY title")
    elif sort_by == 'author':
        c.execute("SELECT * FROM books ORDER BY author")
    else:
        c.execute("SELECT * FROM books")
    books = [{'id': row[0], 'title': row[1], 'author': row[2]} for row in c.fetchall()]
    conn.close()
    return books

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data['title']
    author = data['author']
    book_id = insert_book(title, author)
    return jsonify({'id': book_id}), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    delete_book(book_id)
    return jsonify({'result': True})

@app.route('/books', methods=['GET'])
def get_all_books():
    sort_by = request.args.get('sort')
    books = get_books(sort_by)
    return jsonify(books)

if __name__ == '__main__':
    create_table()
    app.run()
