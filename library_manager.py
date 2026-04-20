import datetime
from database_handler import DatabaseHandler
from models import Book, Reader, Transaction

class LibraryManager:
    def __init__(self):
        self.db = DatabaseHandler()
        self.books, self.readers, self.transactions, self.settings = self.db.load()
        self.fine_per_day = self.settings.get("fine_per_day", 5000)

    def save_all(self):
        self.db.save(self.books, self.readers, self.transactions, self.settings)

    def add_book(self, b_id, title, author, category="Chung"):
        self.books[b_id] = Book(b_id, title, author, category)
        self.save_all()

    def add_reader(self, r_id, name, contact):
        self.readers[r_id] = Reader(r_id, name, contact, max_books=self.settings["max_books"])
        self.save_all()

    def search_books(self, kw):
        kw = kw.lower()
        return [b for b in self.books.values() if kw in b.title.lower() or kw in b.author.lower()]
    
    def search_readers(self, kw):
        kw = kw.lower()
        return [r for r in self.readers.values() if kw in r.name.lower() or kw in r.reader_id.lower()]

    def borrow_book(self, r_id, b_id):
        reader, book = self.readers.get(r_id), self.books.get(b_id)
        if not reader or not book: return "❌ Sai mã độc giả hoặc sách."
        if book.is_borrowed: return "❌ Sách đã có người mượn."
        if not reader.can_borrow(): return "❌ Đạt giới hạn mượn."

        due = datetime.date.today() + datetime.timedelta(days=14)
        book.is_borrowed, book.due_date, book.borrower_id = True, str(due), r_id
        reader.currently_borrowed += 1
        self.transactions.append(Transaction(r_id, b_id, "MƯỢN"))
        self.save_all()
        return f"✅ Thành công! Hạn trả: {due}"

    def return_book(self, r_id, b_id):
        reader, book = self.readers.get(r_id), self.books.get(b_id)
        if not (reader and book and book.borrower_id == r_id): return None
        
        fine = 0
        if book.due_date:
            due_obj = datetime.datetime.strptime(book.due_date, "%Y-%m-%d").date()
            if datetime.date.today() > due_obj:
                fine = (datetime.date.today() - due_obj).days * self.fine_per_day

        book.is_borrowed, book.due_date, book.borrower_id = False, None, None
        reader.currently_borrowed -= 1
        self.transactions.append(Transaction(r_id, b_id, "TRẢ", fine=fine))
        self.save_all()
        return fine
    
    def borrow_multiple_books(self, r_id, b_ids_list):
        """b_ids_list: danh sách các mã sách ['S1', 'S2']"""
        results = []
        reader = self.readers.get(r_id)
        
        if not reader:
            return "❌ Mã độc giả không tồn tại."

        for b_id in b_ids_list:
            b_id = b_id.strip()
            book = self.books.get(b_id)
            
            if not book:
                results.append(f"❓ {b_id}: Không tìm thấy")
                continue
            if book.is_borrowed:
                results.append(f"❌ {b_id}: Đã có người mượn")
                continue
            if not reader.can_borrow():
                results.append(f"🚫 {b_id}: Đã đạt giới hạn mượn")
                break # Dừng vì độc giả không mượn thêm được nữa
            
            # Tiến hành mượn
            due = datetime.date.today() + datetime.timedelta(days=14)
            book.is_borrowed, book.due_date, book.borrower_id = True, str(due), r_id
            reader.currently_borrowed += 1
            self.transactions.append(Transaction(r_id, b_id, "MƯỢN"))
            results.append(f"✅ {book.title}: OK")

        self.save_all()
        return "\n".join(results)

    def return_multiple_books(self, r_id, b_ids_list):
        total_fine = 0
        returned_titles = []
        
        for b_id in b_ids_list:
            fine = self.return_book(r_id, b_id)
            if fine is not None:
                total_fine += fine
                returned_titles.append(self.books[b_id].title)
                
        return returned_titles, total_fine

    def update_settings(self, max_b, fine):
        self.settings = {"max_books": max_b, "fine_per_day": fine}
        self.fine_per_day = fine
        for r in self.readers.values(): r.max_books = max_b
        self.save_all()
        return "✅ Đã cập nhật hệ thống."