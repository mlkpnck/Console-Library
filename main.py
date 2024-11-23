import json
import os
from typing import List, Dict, Any


class Book:
    def __init__(self, title: str, author: str, year: int):
        self.id = None  # будет установлен при добавлении в библиотеку
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for book_data in data:
                    book = Book(book_data['title'], book_data['author'], book_data['year'])
                    book.id = book_data['id']
                    book.status = book_data['status']
                    self.books.append(book)

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        new_book = Book(title, author, year)
        new_book.id = len(self.books) + 1  # Генерация уникального ID
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: int):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return
        raise ValueError("Книга с таким ID не найдена.")

    def search_books(self, query: str) -> List[Book]:
        results = []
        for book in self.books:
            if (query.lower() in book.title.lower() or
                    query.lower() in book.author.lower() or
                    query == str(book.year)):
                results.append(book)
        return results

    def display_books(self):
        for book in self.books:
            print(
                f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

    def change_status(self, book_id: int, new_status: str):
        if new_status not in ["в наличии", "выдана"]:
            raise ValueError("Неверный статус. Доступные статусы: 'в наличии', 'выдана'.")

        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                return
        raise ValueError("Книга с таким ID не найдена.")


def main():
    library = Library('data.json')

    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        command = input("Введите номер команды: ")

        try:
            if command == '1':
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)
                print("Книга успешно добавлена.")

            elif command == '2':
                book_id = int(input("Введите ID книги для удаления: "))
                library.remove_book(book_id)
                print("Книга успешно удалена.")
            elif command == '3':
                query = input("Введите название, автора или год для поиска: ")
                results = library.search_books(query)
                if results:
                    print("Результаты поиска:")
                    for book in results:
                        print(
                            f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")
                else:
                    print("Книги не найдены.")

            elif command == '4':
                library.display_books()

            elif command == '5':
                book_id = int(input("Введите ID книги для изменения статуса: "))
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                library.change_status(book_id, new_status)
                print("Статус книги изменен.")

            elif command == '6':
                print("Выход из программы.")
                break

            else:
                print("Неверная команда. Пожалуйста, попробуйте снова.")

        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
