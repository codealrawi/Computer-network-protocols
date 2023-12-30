import socket
import threading

# Function to add a book
def add_book(client_socket):
    title = input('Enter the title of the book: ')
    message = f'ADD {title}'
    client_socket.send(message.encode('utf-8'))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('localhost', 8000))

while True:
    # Display a menu for the user
    print('1. Add a book')
    print('2. View all books')
    print('3. Quit')
    choice = input('Enter your choice: ')

    # Send user input to the server
    if choice == '1':
        # Create two threads to add two books at the same time
        thread1 = threading.Thread(target=add_book, args=(client_socket,))
        thread2 = threading.Thread(target=add_book, args=(client_socket,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

    elif choice == '2':
        client_socket.send(b'VIEW')
        response = client_socket.recv(1024)
        print(response.decode('utf-8'))

    elif choice == '3':
        client_socket.close()
        break

    else:
        print('Invalid choice.\n')

print('Goodbye!')
