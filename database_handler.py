import sqlite3
import os
from models import Book, Reader, Transaction

class DatabaseHandler:
    def __init__(self, db_path="data/library.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_tables()

    def _get_connection(self):
        """Tạo kết nối tới SQLite và trả về đối tượng connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Truy xuất dữ liệu theo tên cột
        return conn

    def _create_tables(self):
        """Khởi tạo cấu trúc bảng nếu chưa có, bám sát các thuộc tính trong models.py."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Bảng Sách
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                book_id TEXT PRIMARY KEY, 
                                title TEXT, 
                                author TEXT, 
                                category TEXT,
                                is_borrowed INTEGER,
                                due_date TEXT,
                                borrower_id TEXT)''')
            
            # Bảng Độc giả
            cursor.execute('''CREATE TABLE IF NOT EXISTS readers (
                                reader_id TEXT PRIMARY KEY, 
                                name TEXT, 
                                contact TEXT,
                                max_books INTEGER,
                                currently_borrowed INTEGER)''')
            
            # Bảng Giao dịch
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                reader_id TEXT,
                                book_id TEXT,
                                action TEXT,
                                fine INTEGER,
                                timestamp TEXT,
                                cancelled INTEGER DEFAULT 0)''')
            
            # Bảng Cài đặt
            cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                                key TEXT PRIMARY KEY, 
                                value TEXT)''')
            
            # Migration: Thêm cột cancelled nếu chưa có (tương thích DB cũ)
            try:
                cursor.execute("ALTER TABLE transactions ADD COLUMN cancelled INTEGER DEFAULT 0")
            except sqlite3.OperationalError:
                pass  # Cột đã tồn tại, bỏ qua
            
            conn.commit()

    def save_book(self, book):
        """Lưu một cuốn sách vào SQLite."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                REPLACE INTO books (book_id, title, author, category, is_borrowed, due_date, borrower_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (book.book_id, book.title, book.author, book.category, 
                  int(book.is_borrowed), book.due_date, book.borrower_id))
            conn.commit()

    def save_reader(self, reader):
        """Lưu một độc giả vào SQLite."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                REPLACE INTO readers (reader_id, name, contact, max_books, currently_borrowed) 
                VALUES (?, ?, ?, ?, ?)
            """, (reader.reader_id, reader.name, reader.contact, reader.max_books, reader.currently_borrowed))
            conn.commit()

    def add_transaction(self, transaction):
        """Thêm một giao dịch vào SQLite."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (reader_id, book_id, action, fine, timestamp, cancelled) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (transaction.reader_id, transaction.book_id, transaction.action, 
                  transaction.fine, transaction.timestamp, int(transaction.cancelled)))
            conn.commit()

    def save_settings(self, settings):
        """Lưu cài đặt vào SQLite."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for key, value in settings.items():
                cursor.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
            conn.commit()

    def save_all(self, books, readers, transactions, settings):
        """Lưu toàn bộ trạng thái dữ liệu vào SQLite."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Lưu Sách
            for book in books.values():
                cursor.execute("""
                    REPLACE INTO books (book_id, title, author, category, is_borrowed, due_date, borrower_id) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (book.book_id, book.title, book.author, book.category, 
                      int(book.is_borrowed), book.due_date, book.borrower_id))
            
            # Lưu Độc giả
            for reader in readers.values():
                cursor.execute("""
                    REPLACE INTO readers (reader_id, name, contact, max_books, currently_borrowed) 
                    VALUES (?, ?, ?, ?, ?)
                """, (reader.reader_id, reader.name, reader.contact, reader.max_books, reader.currently_borrowed))
            
            # Lưu Giao dịch (Lưu ý: KHÔNG dùng REPLACE vì nó sẽ thay đổi ID tự tăng thành ID người dùng nhập)
            # Ta nên xóa bảng transactions cũ đi chép lại để đảm bảo sạch sẽ.
            cursor.execute("DELETE FROM transactions")
            for t in transactions:
                cursor.execute("""
                    INSERT INTO transactions (reader_id, book_id, action, fine, timestamp, cancelled) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (t.reader_id, t.book_id, t.action, t.fine, t.timestamp, int(t.cancelled)))

            # Lưu Cài đặt
            for key, value in settings.items():
                cursor.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
            
            conn.commit()

    def load(self):
        """Đọc dữ liệu từ SQLite và khởi tạo lại các object Python."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Load Books
                cursor.execute("SELECT * FROM books")
                books = {}
                for row in cursor.fetchall():
                    row_dict = dict(row)
                    row_dict['is_borrowed'] = bool(row_dict['is_borrowed']) # Ép kiểu lại thành boolean
                    books[row_dict['book_id']] = Book(**row_dict)
                
                # Load Readers
                cursor.execute("SELECT * FROM readers")
                readers = {row['reader_id']: Reader(**dict(row)) for row in cursor.fetchall()}
                
                # Load Transactions (Không load cột id tự tăng của SQL vào class)
                cursor.execute("SELECT reader_id, book_id, action, fine, timestamp, cancelled FROM transactions")
                transactions = []
                for row in cursor.fetchall():
                    row_dict = dict(row)
                    row_dict['cancelled'] = bool(row_dict['cancelled'])
                    transactions.append(Transaction(**row_dict))
                
                # Load Settings
                cursor.execute("SELECT * FROM settings")
                settings = {row['key']: (int(row['value']) if row['value'].isdigit() else row['value']) 
                            for row in cursor.fetchall()}
                
                if not settings:
                    settings = {"max_books": 5, "fine_per_day": 5000, "borrow_days": 14}
                elif "borrow_days" not in settings: # Trường hợp user cũ đã có db nhưng chưa có key này
                    settings["borrow_days"] = 14
                    
                return books, readers, transactions, settings
        except Exception as e:
            print(f"Lỗi khi load DB: {e}")
            return {}, {}, [], {"max_books": 5, "fine_per_day": 5000, "borrow_days": 14}

    def delete_book(self, book_id):
        """Xóa một cuốn sách khỏi database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            conn.commit()

    def delete_reader(self, reader_id):
        """Xóa một độc giả khỏi database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM readers WHERE reader_id = ?", (reader_id,))
            conn.commit()

    def cancel_transaction(self, reader_id, book_id, timestamp):
        """
        Đánh dấu một giao dịch là đã hủy trong database (không xóa).

        Sử dụng bộ ba (reader_id, book_id, timestamp) để xác định chính xác
        giao dịch cần hủy.

        Args:
            reader_id (str): Mã độc giả.
            book_id (str): Mã sách.
            timestamp (str): Thời gian giao dịch.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE transactions SET cancelled = 1 WHERE reader_id = ? AND book_id = ? AND timestamp = ?",
                (reader_id, book_id, timestamp)
            )
            conn.commit()

    def reset_database(self):
        """
        Xóa toàn bộ dữ liệu trong database nhưng giữ nguyên cấu trúc bảng.

        Thao tác này sẽ xóa sạch tất cả sách, độc giả, giao dịch và cài đặt,
        sau đó khôi phục lại các giá trị cài đặt mặc định.

        Returns:
            dict: Cài đặt mặc định sau khi reset.
        """
        default_settings = {"max_books": 5, "fine_per_day": 5000, "borrow_days": 14}
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books")
            cursor.execute("DELETE FROM readers")
            cursor.execute("DELETE FROM transactions")
            cursor.execute("DELETE FROM settings")
            # Khôi phục cài đặt mặc định
            for key, value in default_settings.items():
                cursor.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
            conn.commit()
        return default_settings
