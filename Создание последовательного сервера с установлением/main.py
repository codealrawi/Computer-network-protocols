import socket


def handle_client(client_socket):
    # receive data from the client
    data = client_socket.recv(1024)
    data = data.decode()
    data = data.split()
    num1 = int(data[0])
    num2 = int(data[1])
    operation = data[2]

    # perform the appropriate mathematical operation
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        result = num1 / num2
    else:
        result = "Invalid operation"

    # send the result back to the client
    client_socket.send(str(result).encode())
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1234))
    server_socket.listen(5)
    print("Server started")

    while True:
        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)
        handle_client(client_socket)


start_server()
