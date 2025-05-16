class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class BookNotAvailableError(Exception):
    pass


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_lent:
                book.is_lent = True
                return book
        raise BookNotAvailableError("Book is not available or already lent.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.is_lent = False
                return

    def __iter__(self):
        self._index = 0
        self._available_books = [book for book in self.books if not book.is_lent]
        return self

    def __next__(self):
        if self._index < len(self._available_books):
            book = self._available_books[self._index]
            self._index += 1
            return book
        raise StopIteration

    def books_by_author(self, author):
        for book in self.books:
            if book.author.lower() == author.lower():
                yield book


class DigitalLibrary(Library):
    def __init__(self):
        super().__init__()
        self.ebooks = []

    def add_ebook(self, title, author, isbn, size_mb):
        ebook = EBook(title, author, isbn, size_mb)
        self.ebooks.append(ebook)
        self.books.append(ebook)


class EBook(Book):
    def __init__(self, title, author, isbn, size_mb):
        super().__init__(title, author, isbn)
        self.size_mb = size_mb

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Size: {self.size_mb}MB)"

