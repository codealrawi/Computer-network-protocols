import socket
import sys

# Хост и порт сервера
HOST = 'localhost'
PORT = 12345

# Создание сокета и установка соединения
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Функция для отправки сообщений на сервер
def send_message(message):
    sock.sendall(message.encode())

def receive_response():
    data = sock.recv(1024).decode()
    if not data:
        return 'Error: Empty response from server'
    return data

# Главный цикл клиента
while True:
    # Вывод меню
    print('1. Поиск книги')
    print('2. Добавление книги')
    print('3. Удаление книги')
    print('4. Сортировка книг')
    print('5. Выход')

    # Ввод команды
    choice = input('Введите номер команды: ')

    # Обработка выбранной команды
    if choice == '1':
        search_by = input('Введите признак поиска (название, автор, год издания): ')
        value = input('Введите значение: ')
        message = f'search,{search_by},{value}'
        send_message(message)
        response = receive_response()
        print(response)

    elif choice == '2':
        title = input('Введите название книги: ')
        author = input('Введите автора книги: ')
        year = input('Введите год издания книги: ')
        message = f'add,{title},{author},{year}'
        send_message(message)
        response = receive_response()
        print(response)

    elif choice == '3':
        title = input('Введите название книги: ')
        author = input('Введите автора книги: ')
        year = input('Введите год издания книги: ')
        message = f'delete,{title},{author},{year}'
        send_message(message)
        response = receive_response()
        print(response)

    elif choice == '4':
        sort_by = input('Введите признак сортировки (название, автор, год издания): ')
        message = f'sort,{sort_by}'
        send_message(message)
        response = receive_response()
        print(response)

    elif choice == '5':
        # Закрытие соединения и выход из программы
        sock.close()
        sys.exit()

    else:
        print('Неверный номер команды. Повторите ввод.')
