import datetime
from database_handler import DatabaseHandler
from models import Book, Reader, Transaction
from dsa_structures import DoublyLinkedList

class LibraryManager:
    """
    Lớp quản lý nghiệp vụ chính của hệ thống thư viện.

    Lớp này điều phối các hoạt động như mượn/trả sách (bao gồm cả xử lý hàng loạt),
    tìm kiếm dữ liệu, quản lý độc giả và cập nhật cài đặt hệ thống. Nó đóng vai trò
    trung gian giữa giao diện người dùng (GUI) và bộ xử lý dữ liệu (DatabaseHandler).
    """
    def __init__(self):
        """
        Khởi tạo quản lý thư viện và tải dữ liệu từ bộ nhớ.

        Khởi tạo đối tượng DatabaseHandler, sau đó tải danh sách sách, độc giả,
        giao dịch và các cấu hình hệ thống từ file lưu trữ.
        """
        self.db = DatabaseHandler()
        self.books, self.readers, trans_list, self.settings = self.db.load()
        self.transactions = DoublyLinkedList()
        for t in trans_list:
            self.transactions.append(t)
        self.fine_per_day = self.settings.get("fine_per_day", 5000)
        self.borrow_days = self.settings.get("borrow_days", 14)

    def save_all(self):
        """
        Ghi lại toàn bộ trạng thái hiện tại của dữ liệu xuống file.

        Được gọi sau mỗi thao tác thay đổi dữ liệu (thêm sách, mượn/trả) 
        để đảm bảo tính đồng nhất của dữ liệu.
        """
        self.db.save_all(self.books, self.readers, self.transactions, self.settings)

    def add_book(self, b_id, title, author):
        """
        Thêm một cuốn sách mới vào hệ thống.

        Args:
            b_id (str): Mã định danh duy nhất của sách.
            title (str): Tên sách.
            author (str): Tác giả sách.

        Returns:
            tuple: (bool, str) - Thành công/thất bại và thông báo.
        """
        if b_id in self.books:
            return False, f"Mã sách '{b_id}' đã tồn tại trong hệ thống!"
        
        self.books[b_id] = Book(b_id, title, author)
        self.save_all()
        return True, "Đã thêm sách vào kho."

    def add_reader(self, r_id, name, contact):
        """
        Đăng ký một độc giả mới vào hệ thống.

        Args:
            r_id (str): Mã định danh duy nhất của độc giả.
            name (str): Họ và tên độc giả.
            contact (str): Thông tin liên lạc (SĐT/Email).

        Returns:
            tuple: (bool, str) - Thành công/thất bại và thông báo.
        """
        if r_id in self.readers:
            return False, f"Mã độc giả '{r_id}' đã tồn tại trong hệ thống!"
        
        self.readers[r_id] = Reader(r_id, name, contact, max_books=self.settings["max_books"])
        self.save_all()
        return True, "Đã đăng ký độc giả mới."

    def search_books(self, kw):
        """
        Tìm kiếm sách theo từ khóa trong tiêu đề hoặc tên tác giả.

        Args:
            kw (str): Từ khóa tìm kiếm.

        Returns:
            list: Danh sách các đối tượng Book khớp với từ khóa.
        """
        kw = kw.lower()
        return [b for b in self.books.values() if kw in b.title.lower() or kw in b.author.lower()]
    
    def search_readers(self, kw):
        """
        Tìm kiếm độc giả theo tên hoặc mã độc giả.

        Args:
            kw (str): Từ khóa tìm kiếm.

        Returns:
            list: Danh sách các đối tượng Reader khớp với từ khóa.
        """
        kw = kw.lower()
        return [r for r in self.readers.values() if kw in r.name.lower() or kw in r.reader_id.lower()]

    def borrow_book(self, r_id, b_id):
        """
        Xử lý quy trình mượn một cuốn sách lẻ.

        Kiểm tra sự tồn tại của độc giả/sách, trạng thái sách đã mượn chưa 
        và giới hạn mượn của độc giả.

        Args:
            r_id (str): Mã độc giả.
            b_id (str): Mã sách.

        Returns:
            tuple: (bool, str) - Thành công/thất bại và thông báo.
        """
        reader, book = self.readers.get(r_id), self.books.get(b_id)
        if not reader or not book: return False, "Sai mã độc giả hoặc sách."
        if book.is_borrowed: return False, "Sách đã có người mượn."
        if not reader.can_borrow(): return False, "Đạt giới hạn mượn."

        due = datetime.date.today() + datetime.timedelta(days=self.borrow_days)
        book.is_borrowed, book.due_date, book.borrower_id = True, str(due), r_id
        reader.currently_borrowed += 1
        self.transactions.append(Transaction(r_id, b_id, "MƯỢN"))
        self.save_all()
        return True, f"Thành công! Hạn trả: {due}"

    def return_book(self, r_id, b_id):
        """
        Xử lý quy trình trả một cuốn sách và tính toán tiền phạt.

        Args:
            r_id (str): Mã độc giả trả sách.
            b_id (str): Mã sách được trả.

        Returns:
            int/None: Số tiền phạt (nếu có) hoặc None nếu thông tin không hợp lệ.
        """
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
        """
        Thực hiện mượn danh sách nhiều cuốn sách cùng lúc.

        Duyệt qua danh sách mã sách, kiểm tra điều kiện mượn cho từng cuốn 
        và dừng lại nếu độc giả đạt giới hạn mượn tối đa.

        Args:
            r_id (str): Mã độc giả.
            b_ids_list (list): Danh sách các chuỗi mã ID sách.

        Returns:
            tuple: (bool, str) - Thành công/thất bại và thông báo chi tiết.
        """
        results = []
        reader = self.readers.get(r_id)
        
        if not reader:
            return False, "Mã độc giả không tồn tại."

        has_success = False
        for b_id in b_ids_list:
            b_id = b_id.strip()
            book = self.books.get(b_id)
            
            if not book:
                results.append(f"{b_id}: Không tìm thấy")
                continue
            if book.is_borrowed:
                results.append(f"{b_id}: Đã có người mượn")
                continue
            if not reader.can_borrow():
                results.append(f"{b_id}: Đã đạt giới hạn mượn")
                break # Dừng vì độc giả không mượn thêm được nữa
            
            # Tiến hành mượn
            due = datetime.date.today() + datetime.timedelta(days=self.borrow_days)
            book.is_borrowed, book.due_date, book.borrower_id = True, str(due), r_id
            reader.currently_borrowed += 1
            self.transactions.append(Transaction(r_id, b_id, "MƯỢN"))
            results.append(f"{book.title}: Thành công")
            has_success = True

        self.save_all()
        return has_success, "\n".join(results)

    def return_multiple_books(self, r_id, b_ids_list):
        """
        Thực hiện trả nhiều cuốn sách cùng lúc và tổng hợp tiền phạt.

        Args:
            r_id (str): Mã độc giả.
            b_ids_list (list): Danh sách các mã ID sách muốn trả.

        Returns:
            tuple: (returned_titles, total_fine) 
                - returned_titles (list): Tên các cuốn sách đã trả thành công.
                - total_fine (int): Tổng số tiền phạt quá hạn của tất cả các cuốn.
        """
        total_fine = 0
        returned_titles = []
        
        for b_id in b_ids_list:
            fine = self.return_book(r_id, b_id)
            if fine is not None:
                total_fine += fine
                returned_titles.append(self.books[b_id].title)
                
        return returned_titles, total_fine

    def update_settings(self, max_b, fine, borrow_days):
        """
        Cập nhật cấu hình toàn hệ thống về giới hạn mượn và đơn giá phạt.

        Thay đổi này sẽ được áp dụng ngay lập tức cho tất cả dữ liệu độc giả hiện có.

        Args:
            max_b (int): Giới hạn số lượng sách mượn mới.
            fine (int): Số tiền phạt mới cho mỗi ngày quá hạn.
            borrow_days (int): Số ngày được mượn sách.

        Returns:
            str: Thông báo xác nhận cập nhật thành công.
        """
        self.settings = {"max_books": max_b, "fine_per_day": fine, "borrow_days": borrow_days}
        self.fine_per_day = fine
        self.borrow_days = borrow_days
        for r in self.readers.values(): r.max_books = max_b
        self.save_all()
        return True, "Đã cập nhật hệ thống."

    def delete_book(self, b_id):
        """Xóa sách khỏi hệ thống nếu sách chưa bị mượn."""
        book = self.books.get(b_id)
        if not book:
            return False, "Không tìm thấy sách."
        if book.is_borrowed:
            return False, "Sách đang được mượn, không thể xóa. Hãy yêu cầu trả sách trước!"
        
        del self.books[b_id] # Xóa khỏi bộ nhớ
        self.db.delete_book(b_id) # Xóa khỏi database SQLite
        return True, "Xóa sách thành công."

    def delete_reader(self, r_id):
        """Xóa độc giả khỏi hệ thống nếu họ đã trả hết sách."""
        reader = self.readers.get(r_id)
        if not reader:
            return False, "Không tìm thấy độc giả."
        if reader.currently_borrowed > 0:
            return False, "Độc giả này đang giữ sách thư viện, không thể xóa!"
        
        del self.readers[r_id] # Xóa khỏi bộ nhớ
        self.db.delete_reader(r_id) # Xóa khỏi database SQLite
        return True, "Xóa độc giả thành công."

    def edit_book(self, b_id, new_title, new_author):
        """
        Cập nhật thông tin của một cuốn sách đã tồn tại.

        Chỉ cho phép sửa tên sách, tác giả. Mã sách (ID) không thể thay đổi.

        Args:
            b_id (str): Mã sách cần sửa.
            new_title (str): Tên sách mới.
            new_author (str): Tác giả mới.

        Returns:
            tuple: (bool, str) - Thành công/thất bại và thông báo.
        """
        book = self.books.get(b_id)
        if not book:
            return False, "Không tìm thấy sách."
        
        book.title = new_title
        book.author = new_author
        self.db.save_book(book)
        return True, "Cập nhật thông tin sách thành công."

    def edit_reader(self, r_id, new_name, new_contact):
        """
        Cập nhật thông tin của một độc giả đã tồn tại.

        Chỉ cho phép sửa họ tên và thông tin liên lạc. Mã độc giả (ID) không thể thay đổi.

        Args:
            r_id (str): Mã độc giả cần sửa.
            new_name (str): Họ tên mới.
            new_contact (str): Thông tin liên lạc mới.

        Returns:
            tuple: (bool, str) - Thành công/thất bại và thông báo.
        """
        reader = self.readers.get(r_id)
        if not reader:
            return False, "Không tìm thấy độc giả."
        
        reader.name = new_name
        reader.contact = new_contact
        self.db.save_reader(reader)
        return True, "Cập nhật thông tin độc giả thành công."

    def cancel_transaction(self, reader_id, book_id, action, timestamp):
        """
        Hủy một giao dịch và hoàn tác trạng thái sách/độc giả.

        Giao dịch không bị xóa khỏi database mà chỉ được đánh dấu là đã hủy.
        - Nếu hủy giao dịch MƯỢN: trả sách về trạng thái sẵn có, giảm số sách đang mượn.
        - Nếu hủy giao dịch TRẢ: đặt sách về trạng thái đã mượn, tăng số sách đang mượn.

        Args:
            reader_id (str): Mã độc giả.
            book_id (str): Mã sách.
            action (str): Loại giao dịch ("MƯỢN" hoặc "TRẢ").
            timestamp (str): Thời gian giao dịch.

        Returns:
            tuple: (bool, str) - Thành công/thất bại và thông báo.
        """
        # Tìm giao dịch trong danh sách bộ nhớ
        target = None
        for t in self.transactions:
            if t.reader_id == reader_id and t.book_id == book_id and t.timestamp == timestamp:
                target = t
                break
        
        if not target:
            return False, "Không tìm thấy giao dịch."
        
        if target.cancelled:
            return False, "Giao dịch này đã được hủy trước đó."

        book = self.books.get(book_id)
        reader = self.readers.get(reader_id)

        if action == "MƯỢN":
            # Hoàn tác mượn: trả sách về kho
            if book and book.is_borrowed and book.borrower_id == reader_id:
                book.is_borrowed, book.due_date, book.borrower_id = False, None, None
                self.db.save_book(book)
            if reader and reader.currently_borrowed > 0:
                reader.currently_borrowed -= 1
                self.db.save_reader(reader)
        elif action == "TRẢ":
            # Hoàn tác trả: đặt sách về trạng thái đã mượn
            if book and not book.is_borrowed:
                due = datetime.date.today() + datetime.timedelta(days=self.borrow_days)
                book.is_borrowed, book.due_date, book.borrower_id = True, str(due), reader_id
                self.db.save_book(book)
            if reader:
                reader.currently_borrowed += 1
                self.db.save_reader(reader)

        # Đánh dấu hủy trong bộ nhớ và database (không xóa)
        target.cancelled = True
        self.db.cancel_transaction(reader_id, book_id, timestamp)
        return True, "Đã hủy giao dịch thành công."

    def reset_all(self):
        """
        Xóa toàn bộ dữ liệu và khôi phục hệ thống về trạng thái ban đầu.

        Xóa sạch sách, độc giả, giao dịch trong database và bộ nhớ,
        đồng thời đặt lại các cài đặt về giá trị mặc định.
        """
        self.settings = self.db.reset_database()
        self.books = {}
        self.readers = {}
        self.transactions = DoublyLinkedList()
        self.fine_per_day = self.settings["fine_per_day"]
        self.borrow_days = self.settings["borrow_days"]