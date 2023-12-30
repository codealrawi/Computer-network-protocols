import socket
import os
import sys
import multiprocessing
import sqlite3

def handle_client(client_socket, db_conn):
    """
    Обработчик клиентского соединения
    """
    while True:
        # Получение данных от клиента
        request = client_socket.recv(1024).decode('utf-8')

        # Обработка запроса
        if request == 'exit':
            break
        elif request.startswith('search_author:'):
            author = request.split(':')[1]
            cursor = db_conn.execute('SELECT * FROM books WHERE author=?', (author,))
            books = cursor.fetchall()
            response = str(books)
        elif request.startswith('search_year:'):
            year = request.split(':')[1]
            cursor = db_conn.execute('SELECT * FROM books WHERE year=?', (year,))
            books = cursor.fetchall()
            response = str(books)
        elif request.startswith('add_book:'):
            book_data = request.split(':')[1].split(',')
            db_conn.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', book_data)
            db_conn.commit()
            response = 'OK'
        elif request.startswith('delete_book:'):
            book_id = request.split(':')[1]
            db_conn.execute('DELETE FROM books WHERE id=?', (book_id,))
            db_conn.commit()
            response = 'OK'
        elif request.startswith('sort_by_title'):
            cursor = db_conn.execute('SELECT * FROM books ORDER BY title')
            books = cursor.fetchall()
            response = str(books)
        elif request.startswith('sort_by_author'):
            cursor = db_conn.execute('SELECT * FROM books ORDER BY author')
            books = cursor.fetchall()
            response = str(books)
        elif request.startswith('sort_by_year'):
            cursor = db_conn.execute('SELECT * FROM books ORDER BY year')
            books = cursor.fetchall()
            response = str(books)
        else:
            response = 'Invalid request'

        # Отправка ответа клиенту
        client_socket.send(response.encode('utf-8'))

    # Закрытие соединения с клиентом
    client_socket.close()
def run_server():
    # Создание сокета
    global i
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязка сокета к адресу и порту
    server_socket.bind(('0.0.0.0', 2345'))
    #Прослушивание порта
    server_socket.listen()

    # Создание соединения с базой данных
    db_conn = sqlite3.connect('books.db')

    # Создание процессов для обработки клиентских запросов
    num_workers = multiprocessing.cpu_count()
    for i in range(num_workers):
        worker = multiprocessing.Process(target=handle_client, args=(db_conn,))
        worker.start()

    # Ожидание клиентских соединений
    while True:
        client_socket, addr = server_socket.accept()
        print(f'New connection from {addr}')

        #Поиск свободного процесса для обработки клиентского запроса
        for i in range(num_workers):
            if multiprocessing.active_children(): continue
        #Отправка клиентского соединения на обработку в свободный процесс
        multiprocessing.active_children()[i].send(client_socket)
        break
    else:
        client_socket.close()
        # Закрытие соединения с базой данных
        db_conn.close()
        if name == 'main':
            run_server()