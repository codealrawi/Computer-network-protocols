import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))

num1 = input("Введите первое число: ")
num2 = input("Введите второе число: ")
operation = input("Введите, какая операция (+, -, *, /): ")

data = f"{num1} {num2} {operation}"
client_socket.send(data.encode())

result = client_socket.recv(1024)
result = result.decode()
print("Результат:", result)

client_socket.close()
