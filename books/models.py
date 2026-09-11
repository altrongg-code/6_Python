class Book:
    def __init__(self, isbn, title, author, is_borrowed = False):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed

    def __str__(self):
        return f"[{self.isbn}] title: {self.title}, author: {self.author}, 대출여부: {self.is_borrowed}"

class PaperBook(Book):
    def __init__(self, isbn, title, author, location, is_borrowed=False):
        super().__init__(isbn, title, author, is_borrowed)
        self.location = location

    def __str__(self):
        return super().__str__()+f", 책 위치: {self.location}"

class EBook(Book):
    def __init__(self, isbn, title, author, file_format, file_size_mb, is_borrowed=False):
        super().__init__(isbn, title, author, is_borrowed)
        self.file_format = file_format
        self.file_size_mb = file_size_mb

    def __str__(self):
        return super().__str__()+f", 파일 형식: {self.file_format}, 파일 용량(MB): {self.file_size_mb}"
