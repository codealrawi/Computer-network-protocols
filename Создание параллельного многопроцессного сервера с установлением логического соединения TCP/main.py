import socket
import multiprocessing
import sqlite3

# Создание соединения с базой данных
conn = sqlite3.connect('books.db')

# Создание курсора для выполнения запросов
cur = conn.cursor()

# Создание таблицы для хранения информации о книгах
cur.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)')

# Добавление книги в базу данных
def add_book(title, author, year):
    cur.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    conn.commit()

# Получение списка всех книг
def get_all_books():
    cur.execute('SELECT * FROM books')
    return cur.fetchall()

# Поиск книг по автору
def search_books_by_author(author):
    cur.execute('SELECT * FROM books WHERE author=?', (author,))
    return cur.fetchall()

# Поиск книг по году издания
def search_books_by_year(year):
    cur.execute('SELECT * FROM books WHERE year=?', (year,))
    return cur.fetchall()

# Удаление книги по id
def remove_book(id):
    cur.execute('DELETE FROM books WHERE id=?', (id,))
    conn.commit()

# Закрытие соединения с базой данных
def close_db():
    conn.close()

# Функция, которая будет выполняться в каждом процессе для обработки запросов клиентов
def handle_client(conn, addr, books):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)  # Получаем данные от клиента
        if not data:
            break
        message = data.decode()  # Декодируем полученные данные
        if message == "get_all":
            # Отправляем клиенту список всех книг в библиотеке
            books_str = "\n".join(str(book) for book in books)
            conn.sendall(books_str.encode())
        elif message.startswith("get_by_author"):
            # Извлекаем имя автора из запроса
            author = message.split()[1]
            # Фильтруем список книг по имени автора
            books_filtered = [book for book in books if book.author == author]
            # Отправляем клиенту список найденных книг
            books_str = "\n".join(str(book) for book in books_filtered)
            conn.sendall(books_str.encode())
        # Реализуйте обработку остальных запросов в соответствии с заданием
    conn.close()
    print(f"Connection with {addr} closed")

if __name__ == "__main__":
    # Создаем сокет для TCP-сервера
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 12345))  # Привязываем сервер к адресу и порту
        s.listen(5)  # Запускаем прослушивание новых соединений
        print("Server started")
        books = []  # Создаем пустой список для хранения книг
        while True:
            # Принимаем новое соединение от клиента
            conn, addr = s.accept()
            # Создаем новый процесс для обработки запросов этого клиента
            p = multiprocessing.Process(target=handle_client, args=(conn, addr, books))
            p.start()
            # Закрываем соединение в родительском процессе, чтобы дочерний процесс мог обрабатывать запросы
            conn.close()
