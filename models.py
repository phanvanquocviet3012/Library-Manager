import datetime

class Book:
    """
    Đại diện cho một cuốn sách trong hệ thống quản lý thư viện.

    Lớp này lưu trữ thông tin cơ bản về sách và theo dõi trạng thái mượn/trả, 
    bao gồm thời hạn trả và người đang giữ sách.
    """
    def __init__(self, book_id, title, author, category="Chung", is_borrowed=False, due_date=None, borrower_id=None):
        """
        Khởi tạo một đối tượng Book mới.

        Args:
            book_id (str): Mã định danh duy nhất (ID) của cuốn sách.
            title (str): Tên hoặc tiêu đề của cuốn sách.
            author (str): Tác giả của cuốn sách.
            category (str, optional): Thể loại sách. Mặc định là "Chung".
            is_borrowed (bool, optional): Trạng thái mượn của sách. 
                True nếu đã bị mượn, False nếu còn trong kho. Mặc định là False.
            due_date (str, optional): Ngày đến hạn trả sách (định dạng YYYY-MM-DD). 
                Mặc định là None.
            borrower_id (str, optional): Mã ID của độc giả đang mượn cuốn sách này. 
                Mặc định là None.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.is_borrowed = is_borrowed
        self.due_date = due_date
        self.borrower_id = borrower_id

    def to_dict(self):
        """
        Chuyển đổi thông tin sách thành một dictionary.

        Thường dùng để chuẩn bị dữ liệu cho việc lưu trữ vào file JSON.

        Returns:
            dict: Dictionary chứa toàn bộ các thuộc tính của đối tượng Book.
        """
        return self.__dict__

class Reader:
    """
    Đại diện cho một độc giả trong hệ thống quản lý thư viện.

    Lớp này chịu trách nhiệm lưu trữ thông tin cá nhân của độc giả và 
    kiểm soát số lượng sách mà độc giả đó đang mượn để đảm bảo không 
    vượt quá giới hạn cho phép.
    """
    def __init__(self, reader_id, name, contact, max_books=5, currently_borrowed=0):
        """
        Khởi tạo một đối tượng Reader mới.

        Args:
            reader_id (str): Mã định danh duy nhất của độc giả.
            name (str): Họ và tên của độc giả.
            contact (str): Thông tin liên lạc (số điện thoại hoặc email).
            max_books (int, optional): Số lượng sách tối đa được phép mượn. 
                Mặc định là 5.
            currently_borrowed (int, optional): Số lượng sách hiện đang mượn. 
                Mặc định là 0.
        """
        self.reader_id = reader_id
        self.name = name
        self.contact = contact
        self.max_books = max_books
        self.currently_borrowed = currently_borrowed

    def can_borrow(self) -> bool:
        """
        Kiểm tra xem độc giả có quyền mượn thêm sách hay không.

        Dựa trên so sánh giữa số lượng sách đang giữ và giới hạn cho phép.

        Returns:
            bool: True nếu số sách đang mượn ít hơn giới hạn (max_books), 
                  ngược lại trả về False.
        """
        return self.currently_borrowed < self.max_books

    def to_dict(self):
        """
        Chuyển đổi thông tin độc giả thành một dictionary.

        Thường dùng để chuẩn bị dữ liệu cho việc lưu trữ vào file JSON.

        Returns:
            dict: Dictionary chứa toàn bộ các thuộc tính của đối tượng Reader.
        """
        return self.__dict__

class Transaction:
    """
    Đại diện cho một bản ghi giao dịch trong hệ thống thư viện.

    Lớp này lưu trữ thông tin về các hoạt động mượn hoặc trả sách, bao gồm 
    thông tin về người thực hiện, đối tượng sách, các khoản phí phát sinh 
    và thời điểm giao dịch diễn ra.
    """
    def __init__(self, reader_id, book_id, action, fine=0, timestamp=None):
        """
        Khởi tạo một đối tượng Transaction mới.

        Args:
            reader_id (str): Mã định danh của độc giả thực hiện giao dịch.
            book_id (str): Mã định danh của cuốn sách liên quan đến giao dịch.
            action (str): Loại hành động thực hiện (ví dụ: "MƯỢN", "TRẢ").
            fine (int, optional): Số tiền phạt phát sinh nếu giao dịch là trả sách quá hạn. 
                Mặc định là 0.
            timestamp (str, optional): Thời gian thực hiện giao dịch định dạng 
                "YYYY-MM-DD HH:MM:SS". Nếu không cung cấp, hệ thống sẽ tự động 
                lấy thời gian hiện tại.
        """
        self.reader_id = reader_id
        self.book_id = book_id
        self.action = action 
        self.fine = fine
        self.timestamp = timestamp or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Chuyển đổi đối tượng Transaction thành một dictionary.

        Phương thức này thường được sử dụng để chuẩn bị dữ liệu trước khi 
        ghi vào file JSON thông qua DatabaseHandler.

        Returns:
            dict: Một dictionary chứa toàn bộ các thuộc tính của giao dịch.
        """
        return self.__dict__