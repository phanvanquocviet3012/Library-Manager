import datetime

class Book:
    def __init__(self, book_id, title, author, category="Chung", is_borrowed=False, due_date=None, borrower_id=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.is_borrowed = is_borrowed
        self.due_date = due_date
        self.borrower_id = borrower_id

    def to_dict(self):
        return self.__dict__

class Reader:
    def __init__(self, reader_id, name, contact, max_books=5, currently_borrowed=0):
        self.reader_id = reader_id
        self.name = name
        self.contact = contact
        self.max_books = max_books
        self.currently_borrowed = currently_borrowed

    def can_borrow(self) -> bool:
        return self.currently_borrowed < self.max_books

    def to_dict(self):
        return self.__dict__

class Transaction:
    def __init__(self, reader_id, book_id, action, fine=0, timestamp=None):
        self.reader_id = reader_id
        self.book_id = book_id
        self.action = action 
        self.fine = fine
        self.timestamp = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        fine_str = f" | Phạt: {self.fine}đ" if self.fine > 0 else ""
        return f"[{self.timestamp}] {self.action}: Độc giả {self.reader_id} - Sách {self.book_id}{fine_str}"