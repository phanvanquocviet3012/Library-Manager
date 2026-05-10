# 📚 Library Manager

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![GUI Library](https://img.shields.io/badge/GUI-CustomTkinter-orange)
![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**Library Manager** là một ứng dụng quản lý thư viện máy tính để bàn (Desktop App) được thiết kế hiện đại, tập trung vào trải nghiệm người dùng. Ứng dụng giúp số hóa việc quản lý sách, độc giả và các giao dịch mượn/trả một cách tự động và chính xác, với kiến trúc dữ liệu an toàn.

## 🚀 Tính năng chính

### 1. Quản lý Kho sách & Độc giả
* **Kho sách:** Thêm mới, sửa đổi thông tin (tên sách, tác giả, thể loại), xóa sách và theo dõi trạng thái (Sẵn có/Đã mượn).
* **Độc giả:** Quản lý thông tin liên lạc, giới hạn số lượng sách tối đa mỗi người được mượn, cùng các chức năng thêm/sửa/xóa độc giả.
* **Tìm kiếm:** Hệ thống tìm kiếm thời gian thực (Search-as-you-type) nhanh chóng cho cả sách và độc giả.
* **Kiểm soát dữ liệu đầu vào:** Tự động kiểm tra trùng lặp mã ID, ngăn chặn người dùng vô tình ghi đè dữ liệu.

### 2. Nghiệp vụ Mượn/Trả thông minh
* **Mượn sách hàng loạt:** Cho phép mượn nhiều mã sách cùng lúc chỉ bằng một thao tác.
* **Trả sách trực quan:** Liệt kê danh sách sách đang mượn kèm Checkbox để chọn trả nhanh chóng.
* **Tính phí phạt:** Tự động tính tiền phạt dựa trên số ngày quá hạn và cấu hình hệ thống.
* **Hủy giao dịch (Hoàn tác):** Chức năng hủy giao dịch mượn/trả an toàn, tự động hoàn tác (rollback) trạng thái của sách và độc giả, lưu vết trên hệ thống với nhãn "ĐÃ HỦY".

### 3. Hệ thống & Lưu trữ
* **Cài đặt:** Tùy chỉnh mức phạt mỗi ngày, giới hạn mượn và số ngày mượn cho phép ngay trên giao diện.
* **Cơ sở dữ liệu:** Sử dụng hệ quản trị cơ sở dữ liệu `SQLite` siêu tốc, tối ưu hóa qua các tác vụ lưu dòng (row-level) thay vì ghi đè toàn bộ dữ liệu.
* **Reset Hệ Thống:** "Vùng nguy hiểm" (Danger Zone) cho phép xóa sạch toàn bộ dữ liệu an toàn với xác nhận bảo mật nhiều lớp.

## 🛠 Kiến trúc dự án (MVC Pattern)

Dự án được thiết kế cấu trúc phân lớp rõ ràng, tách biệt hoàn toàn giữa Giao diện (UI) và Logic Nghiệp vụ (Business Logic) nhằm dễ dàng mở rộng và bảo trì:

* `models.py`: Định nghĩa cấu trúc dữ liệu cơ sở (Book, Reader, Transaction).
* `database_handler.py`: Tầng xử lý dữ liệu (Data Access Layer) thao tác trực tiếp với SQLite.
* `library_manager.py`: Tầng điều phối (Controller) chứa 100% logic nghiệp vụ thuần (không chứa UI/Emoji).
* `gui.py`: Giao diện người dùng (View) xây dựng bằng thư viện CustomTkinter.
* `main.py`: Điểm khởi chạy ứng dụng (Entry point).

## 📦 Cài đặt

1. **Yêu cầu:** Máy tính đã cài đặt Python 3.8 trở lên.
2. **Cài đặt thư viện giao diện:**
   ```bash
   pip install customtkinter
   ```

3. **Khởi chạy ứng dụng:**
   ```bash
   python main.py
   ```

## 📖 Hướng dẫn sử dụng

1. **Khởi tạo:** Khi chạy lần đầu, ứng dụng sẽ tự động tạo file cơ sở dữ liệu `library.db` trong thư mục `data/` (thư mục này đã được gitignore để bảo vệ thông tin người dùng).
2. **Mượn sách:** 
   - Vào mục **Mượn Sách**.
   - Nhập ID độc giả (ví dụ: `R001`).
   - Nhập danh sách ID sách cách nhau bởi dấu phẩy (ví dụ: `B001, B002`).
3. **Trả sách:**
   - Vào mục **Trả Sách**.
   - Nhập ID độc giả và nhấn **Kiểm Tra**.
   - Chọn các cuốn sách muốn trả và nhấn **Xác Nhận**.
4. **Hủy giao dịch:**
   - Vào mục **Lịch Sử Giao Dịch**.
   - Chọn một giao dịch bất kỳ và bấm **Hủy Giao Dịch Đã Chọn**. Hệ thống sẽ tự động khôi phục trạng thái.

## 🤝 Đóng góp

Mọi ý tưởng đóng góp hoặc báo lỗi (issue) xin vui lòng gửi về:

- **Tác giả:** [Phan Văn Quốc Việt](https://github.com/phanvanquocviet3012)
- **Repo:** [Library-Manager](https://github.com/phanvanquocviet3012/Library-Manager)

---