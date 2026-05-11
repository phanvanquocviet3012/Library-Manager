# 📚 Library Manager - Đồ Án DSA

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![GUI Library](https://img.shields.io/badge/GUI-CustomTkinter-orange)
![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey)
![Data Structures](https://img.shields.io/badge/Algorithms-DSA-success)
![License](https://img.shields.io/badge/license-MIT-green)

**Library Manager** là một ứng dụng quản lý thư viện máy tính để bàn (Desktop App) được thiết kế đặc biệt phục vụ cho **Đồ án môn Cấu trúc Dữ liệu và Thuật toán (DSA)**. Ứng dụng không chỉ có giao diện hiện đại mà còn tự cài đặt và tích hợp các cấu trúc dữ liệu, thuật toán chuyên sâu thay vì sử dụng các hàm có sẵn của ngôn ngữ, giúp tối ưu hóa hiệu suất và đáp ứng đúng chuẩn học thuật.

---

## 💡 Điểm Nhấn DSA (Data Structures & Algorithms)

Để đáp ứng yêu cầu của môn học DSA, dự án đã triển khai mã nguồn tự viết trong file `dsa_structures.py` và áp dụng vào logic thực tế của phần mềm:

1. **Doubly Linked List (Danh sách liên kết đôi):**
   - **Ứng dụng:** Quản lý lịch sử giao dịch mượn/trả sách (`self.transactions`).
   - **Ưu điểm:** Khả năng thêm giao dịch mới vào đuôi danh sách ở $O(1)$. Hỗ trợ duyệt ngược từ đuôi lên đầu (bằng hàm `reverse_iter()`) ở độ phức tạp $O(N)$ để hiển thị giao dịch mới nhất lên giao diện mà không cần sao chép hay dùng hàm `reversed()` của Python.

2. **Merge Sort (Sắp xếp Trộn):**
   - **Ứng dụng:** Sắp xếp độ ưu tiên của sách trong bảng hiển thị (Sách quá hạn > Sắp hết hạn > Sẵn có).
   - **Ưu điểm:** Thuật toán chia để trị tự cài đặt, đảm bảo độ phức tạp luôn ở mức tối ưu $O(N \log N)$ (Best/Worst/Average cases) và là một Stable Sort giúp bảo toàn thứ tự tương đối của dữ liệu.

---

## 🚀 Tính năng chính

### 1. Quản lý Kho sách & Độc giả
* **Kho sách:** Thêm mới, sửa đổi thông tin, xóa sách và theo dõi trạng thái Sẵn có/Đã mượn.
* **Độc giả:** Quản lý thông tin liên lạc, giới hạn số lượng sách tối đa mỗi người được mượn.
* **Tìm kiếm:** Hệ thống tìm kiếm thời gian thực (Search-as-you-type) nhanh chóng cho cả sách và độc giả.

### 2. Nghiệp vụ Mượn/Trả thông minh
* **Mượn sách hàng loạt:** Cho phép mượn nhiều mã sách cùng lúc chỉ bằng một thao tác.
* **Trả sách trực quan:** Liệt kê danh sách sách đang mượn kèm Checkbox để chọn trả nhanh chóng.
* **Tính phí phạt:** Tự động tính tiền phạt dựa trên số ngày quá hạn và cấu hình hệ thống.
* **Hủy giao dịch:** Chức năng hủy giao dịch tự động hoàn tác (rollback) trạng thái của sách và độc giả trên CSDL.

### 3. Hệ thống & Lưu trữ
* **Cài đặt:** Tùy chỉnh mức phạt mỗi ngày, giới hạn mượn và số ngày mượn cho phép.
* **Cơ sở dữ liệu:** Hệ quản trị CSDL `SQLite` siêu tốc, tối ưu thao tác lưu dòng (row-level).
* **Reset Hệ Thống:** Chức năng cho phép xóa sạch toàn bộ dữ liệu (Danger Zone) an toàn.
* **Chuẩn hóa Code:** 100% Class và Hàm được chú thích (Docstrings) tiếng Việt theo chuẩn PEP 8.

---

## 🛠 Kiến trúc dự án (MVC Pattern)

Dự án được phân lớp rõ ràng, tách biệt hoàn toàn giữa Giao diện và Logic Nghiệp vụ:

* `models.py`: Định nghĩa cấu trúc dữ liệu cơ sở (Book, Reader, Transaction).
* `dsa_structures.py`: Các cấu trúc dữ liệu và thuật toán tự cài đặt (DoublyLinkedList, Merge Sort).
* `database_handler.py`: Tầng xử lý dữ liệu (Data Access Layer) giao tiếp với SQLite.
* `library_manager.py`: Tầng điều phối (Controller) kết hợp logic nghiệp vụ với dữ liệu.
* `gui.py`: Giao diện người dùng (View) xây dựng bằng thư viện CustomTkinter.
* `main.py`: Điểm khởi chạy ứng dụng (Entry point).

---

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

1. **Khởi tạo:** Khi chạy lần đầu, ứng dụng tự tạo file `library.db` trong thư mục `data/` (đã được gitignore).
2. **Mượn sách:** Nhập ID độc giả và danh sách ID sách cách nhau bởi dấu phẩy.
3. **Trả sách:** Nhập ID độc giả, hệ thống tự load danh sách sách đang mượn -> check chọn để trả.
4. **Hủy giao dịch:** Tại Lịch Sử Giao Dịch, chọn một giao dịch và bấm **Hủy Giao Dịch Đã Chọn**.

## 🤝 Đóng góp

Mọi ý tưởng đóng góp hoặc báo lỗi xin vui lòng gửi về:

- **Tác giả:** [Phan Văn Quốc Việt](https://github.com/phanvanquocviet3012)
- **Repo:** [Library-Manager](https://github.com/phanvanquocviet3012/Library-Manager)