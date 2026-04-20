import json
import os
from models import Book, Reader, Transaction

class DatabaseHandler:
    """
    Lớp xử lý việc lưu trữ và truy xuất dữ liệu từ file hệ thống.

    DatabaseHandler chịu trách nhiệm quản lý việc đọc/ghi dữ liệu vào file JSON,
    đảm bảo thư mục lưu trữ luôn tồn tại và xử lý các tình huống file không hợp lệ 
    để tránh làm hỏng luồng chạy của chương trình.
    """
    def __init__(self, file_path="data/library_data.json"):
        """
        Khởi tạo bộ xử lý cơ sở dữ liệu.

        Args:
            file_path (str, optional): Đường dẫn đến file JSON dùng để lưu trữ dữ liệu. 
                Mặc định là "data/library_data.json".

        Note:
            Hàm khởi tạo sẽ tự động kiểm tra và tạo thư mục chứa file nếu thư mục đó 
            chưa tồn tại trên hệ thống.
        """
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def save(self, books, readers, transactions, settings):
        """
        Chuyển đổi các đối tượng Python thành định dạng JSON và ghi xuống đĩa cứng.

        Phương thức này thực hiện tuần tự hóa (serialization) các đối tượng Book, 
        Reader và Transaction thông qua phương thức `to_dict()` của chúng.

        Args:
            books (dict): Dictionary chứa các đối tượng Book.
            readers (dict): Dictionary chứa các đối tượng Reader.
            transactions (list): Danh sách các đối tượng Transaction.
            settings (dict): Dictionary chứa các cấu hình hệ thống (giới hạn mượn, tiền phạt).
        """
        data = {
            "books": {k: v.to_dict() for k, v in books.items()},
            "readers": {k: v.to_dict() for k, v in readers.items()},
            "transactions": [t.to_dict() for t in transactions],
            "settings": settings
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        """
        Đọc dữ liệu từ file JSON và tái tạo lại các đối tượng Python tương ứng.

        Thực hiện quá trình giải tuần tự hóa (deserialization). Nếu file không tồn tại 
        hoặc dữ liệu bị lỗi, hàm sẽ trả về các cấu trúc dữ liệu rỗng và cài đặt mặc định 
        để ứng dụng có thể tiếp tục khởi động.

        Returns:
            tuple: Trả về một tuple gồm 4 thành phần:
                - books (dict): Dictionary chứa các đối tượng Book được tạo từ dữ liệu file.
                - readers (dict): Dictionary chứa các đối tượng Reader được tạo từ dữ liệu file.
                - transactions (list): Danh sách các đối tượng Transaction.
                - settings (dict): Cấu hình hệ thống hiện tại.
        """
        default_settings = {"max_books": 5, "fine_per_day": 5000}
        if not os.path.exists(self.file_path): 
            return {}, {}, [], default_settings
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                books = {k: Book(**v) for k, v in data.get("books", {}).items()}
                readers = {k: Reader(**v) for k, v in data.get("readers", {}).items()}
                transactions = [Transaction(**t) for t in data.get("transactions", [])]
                settings = data.get("settings", default_settings)
                return books, readers, transactions, settings
        except Exception:
            return {}, {}, [], default_settings