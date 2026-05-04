import datetime
from database_handler import DatabaseHandler
from models import Book, Reader, Transaction

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
        self.books, self.readers, self.transactions, self.settings = self.db.load()
        self.fine_per_day = self.settings.get("fine_per_day", 5000)
        self.borrow_days = self.settings.get("borrow_days", 14)

    def save_all(self):
        """
        Ghi lại toàn bộ trạng thái hiện tại của dữ liệu xuống file.

        Được gọi sau mỗi thao tác thay đổi dữ liệu (thêm sách, mượn/trả) 
        để đảm bảo tính đồng nhất của dữ liệu.
        """
        self.db.save(self.books, self.readers, self.transactions, self.settings)

    def add_book(self, b_id, title, author, category="Chung"):
        """
        Thêm một cuốn sách mới vào hệ thống.

        Args:
            b_id (str): Mã định danh duy nhất của sách.
            title (str): Tên sách.
            author (str): Tác giả sách.
            category (str, optional): Thể loại. Mặc định là "Chung".
        """
        self.books[b_id] = Book(b_id, title, author, category)
        self.save_all()

    def add_reader(self, r_id, name, contact):
        """
        Đăng ký một độc giả mới vào hệ thống.

        Args:
            r_id (str): Mã định danh duy nhất của độc giả.
            name (str): Họ và tên độc giả.
            contact (str): Thông tin liên lạc (SĐT/Email).
        """
        self.readers[r_id] = Reader(r_id, name, contact, max_books=self.settings["max_books"])
        self.save_all()

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
            str: Thông báo kết quả mượn sách thành công (kèm hạn trả) hoặc lỗi.
        """
        reader, book = self.readers.get(r_id), self.books.get(b_id)
        if not reader or not book: return "❌ Sai mã độc giả hoặc sách."
        if book.is_borrowed: return "❌ Sách đã có người mượn."
        if not reader.can_borrow(): return "❌ Đạt giới hạn mượn."

        due = datetime.date.today() + datetime.timedelta(days=self.borrow_days)
        book.is_borrowed, book.due_date, book.borrower_id = True, str(due), r_id
        reader.currently_borrowed += 1
        self.transactions.append(Transaction(r_id, b_id, "MƯỢN"))
        self.save_all()
        return f"✅ Thành công! Hạn trả: {due}"

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
            str: Chuỗi văn bản chi tiết kết quả cho từng mã sách đầu vào.
        """
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
            due = datetime.date.today() + datetime.timedelta(days=self.borrow_days                                                                                                              )
            book.is_borrowed, book.due_date, book.borrower_id = True, str(due), r_id
            reader.currently_borrowed += 1
            self.transactions.append(Transaction(r_id, b_id, "MƯỢN"))
            results.append(f"✅ {book.title}: OK")

        self.save_all()
        return "\n".join(results)

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
        return "✅ Đã cập nhật hệ thống."

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