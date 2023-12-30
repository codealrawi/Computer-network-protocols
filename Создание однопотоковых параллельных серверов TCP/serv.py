import socket
import sqlite3
import multiprocessing

# Create a connection to the database
conn = sqlite3.connect('books1.db')
c = conn.cursor()

# Create a table for books if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL)''')

# Start a new process for each client request
def handle_client(client_socket, address):
    print(f'New client connected from {address}')

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        # Add a new book title to the database
        if data.startswith('ADD '):
            title = data[4:]
            c.execute(f"INSERT INTO books (title) VALUES ('{title}')")
            conn.commit()
            client_socket.send(b'Book added successfully.\n')

        # Retrieve all books from the database
        elif data == 'VIEW':
            books = c.execute('SELECT * FROM books').fetchall()
            if len(books) == 0:
                client_socket.send(b'No books found.\n')
            else:
                response = ''
                for book in books:
                    response += f'{book[0]}. {book[1]}\n'
                client_socket.send(response.encode('utf-8'))

        # Delete a book from the database
        elif data.startswith('DELETE '):
            book_id = data[7:]
            c.execute(f"DELETE FROM books WHERE id = {book_id}")
            conn.commit()
            client_socket.send(b'Book deleted successfully.\n')

        # Invalid command
        else:
            client_socket.send(b'Invalid command.\n')

    # Close the connection
    client_socket.close()
    print(f'Connection closed from {address}')

# Start the server
def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a host and port
    server_socket.bind(('localhost', 8000))

    # Listen for incoming connections
    server_socket.listen()

    print('Server started.')

    while True:
        # Accept incoming connections
        client_socket, address = server_socket.accept()

        # Create a new process for each client
        p = multiprocessing.Process(target=handle_client, args=(client_socket, address))
        p.start()

# Call the start_server function
if __name__ == '__main__':
    start_server()
