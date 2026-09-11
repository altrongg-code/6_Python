from models import PaperBook, EBook

class Library:
    def __init__(self):
        self.books = []

    def show_all_books(self):
        return self.books

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        else:
            raise BookNotFoundError()

    def validate_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                raise DuplicatedISBNError()

    # DuplicatedISBNError 예외 발생
    def create_paper_book(self, isbn, title, author, location):
        self.validate_isbn(isbn)
        book = PaperBook(isbn, title, author, location)
        self.books.append(book)
        return book

    # DuplicatedISBNError 예외 발생
    def create_E_book(self, isbn, title, author, file_format, file_size_mb):
        self.validate_isbn(isbn)
        book = EBook(isbn, title, author, file_format, file_size_mb)
        self.books.append(book)
        return book

    # BookNotFoundError 예외 발생
    # AlreadyBorrowedError 예외 발생
    def borrow(self, isbn):
        book = self.find_book_by_isbn(isbn)
        if book.is_borrowed:
            raise AlreadyBorrowedError()
        book.is_borrowed = True
        return book

    # BookNotFoundError 예외 발생
    def return_book(self, isbn):
        book = self.find_book_by_isbn(isbn)
        if not book.is_borrowed:
            return False
        book.is_borrowed = False
        return book
        

    def search_book(self, title = "", author = ""):
        result = []
        for book in self.books:
            if book.is_borrowed:
                continue
            if title:
                if title in book.title:
                    result.append(book)
            if author:
                if author in book.author:
                    result.append(book)
        return result
    # 대출 가능한 도서만 검색

    def show_all_authors(self):
        if not self.books:
            return False
        
        author_list = []
        for book in self.books:
            author_list.append(book.author)
        return set(author_list)

    # BookNotFoundError 예외 발생
    def delete_book(self, isbn):
        book = self.find_book_by_isbn(isbn)
        self.books.remove(book)
        return book
        
        
class DuplicatedISBNError(Exception):
    def __init__(self):
        super().__init__("중복된 ISBN입니다.")

class BookNotFoundError(Exception):
    def __init__(self):
        super().__init__("존재하지 않는 ISBN입니다.")

class AlreadyBorrowedError(Exception):
    def __init__(self):
        super().__init__("이미 대출중인 도서입니다.")