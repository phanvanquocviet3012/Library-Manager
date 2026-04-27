# 📚 Library Manager

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![GUI Library](https://img.shields.io/badge/GUI-CustomTkinter-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**Library Manager** là một ứng dụng quản lý thư viện máy tính để bàn (Desktop App) được thiết kế hiện đại, tập trung vào trải nghiệm người dùng. Ứng dụng giúp số hóa việc quản lý sách, độc giả và các giao dịch mượn/trả một cách tự động và chính xác.

## 🚀 Tính năng chính

### 1. Quản lý Kho sách & Độc giả
* **Kho sách:** Theo dõi danh sách sách, tác giả, thể loại và trạng thái (Sẵn có/Đã mượn).
* **Độc giả:** Quản lý thông tin liên lạc và giới hạn số lượng sách tối đa mỗi người được mượn.
* **Tìm kiếm:** Hệ thống tìm kiếm thời gian thực (Search-as-you-type) cho cả sách và độc giả.

### 2. Nghiệp vụ Mượn/Trả thông minh
* **Mượn sách hàng loạt:** Cho phép mượn nhiều mã sách cùng lúc chỉ bằng một thao tác.
* **Trả sách trực quan:** Liệt kê danh sách sách đang mượn kèm Checkbox để chọn trả nhanh chóng.
* **Tính phí phạt:** Tự động tính tiền phạt dựa trên số ngày quá hạn và cấu hình hệ thống.

### 3. Hệ thống & Lưu trữ
* **Cài đặt:** Tùy chỉnh mức phạt mỗi ngày và giới hạn mượn ngay trên giao diện.
* **Cơ sở dữ liệu:** Lưu trữ dưới dạng file .db và sử dụng SQLite để quản lý dữ liệu.

## 🛠 Kiến trúc dự án (MVC Pattern)

Dự án được cấu trúc theo mô hình phân lớp để dễ dàng bảo trì:

* `models.py`: Định nghĩa cấu trúc dữ liệu (Book, Reader, Transaction).
* `database_handler.py`: Tầng xử lý dữ liệu (Data Access Layer) xử lý file .db.
* `library_manager.py`: Tầng điều phối (Controller) xử lý logic nghiệp vụ.
* `gui.py`: Giao diện người dùng (View) xây dựng bằng CustomTkinter.
* `main.py`: Điểm khởi chạy ứng dụng (Entry point).

## 📦 Cài đặt

1. **Yêu cầu:** Máy tính đã cài đặt Python 3.8 trở lên.
2. **Cài đặt thư viện giao diện:**
   ```bash
   pip install customtkinter
    ````

3.  **Chạy ứng dụng:**
    ```bash
    python main.py
    ```

## 📖 Hướng dẫn sử dụng

1.  **Khởi tạo:** Khi chạy lần đầu, ứng dụng sẽ tự động tạo file dữ liệu trong thư mục `data/`.
2.  **Mượn sách:** - Vào mục **Mượn Sách**.
      - Nhập ID độc giả (ví dụ: `R001`).
      - Nhập danh sách ID sách cách nhau bởi dấu phẩy (ví dụ: `B001, B002`).
3.  **Trả sách:**
      - Vào mục **Trả Sách**.
      - Nhập ID độc giả và nhấn **Kiểm Tra**.
      - Chọn các cuốn sách muốn trả và nhấn **Xác Nhận**.

## 🤝 Đóng góp

Mọi ý tưởng đóng góp hoặc báo lỗi (issue) xin vui lòng gửi về:

  - **Tác giả:** [Phan Văn Quốc Việt](https://www.google.com/search?q=https://github.com/phanvanquocviet3012)
  - **Repo:** [Library-Manager](https://github.com/phanvanquocviet3012/Library-Manager)

-----