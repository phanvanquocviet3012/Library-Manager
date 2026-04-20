import customtkinter as ctk
from tkinter import ttk, messagebox
from library_manager import LibraryManager

class LibraryGUI(ctk.CTk):
    """
    Lớp giao diện người dùng chính cho ứng dụng Quản lý Thư viện.

    Sử dụng thư viện customtkinter để tạo giao diện hiện đại với cấu trúc 
    Sidebar (thanh bên) điều hướng và Content Area (vùng nội dung) thay đổi linh hoạt.
    """
    def __init__(self):
        """
        Khởi tạo cửa sổ ứng dụng và các thành phần giao diện cơ bản.

        Thiết lập tiêu đề, kích thước cửa sổ, khởi tạo đối tượng LibraryManager 
        để xử lý dữ liệu và vẽ bố cục (layout) ban đầu.
        """
        super().__init__()
        self.title("Library Manager - In-Window Interface")
        self.geometry("1100x700")
        self.manager = LibraryManager()
        
        self.return_check_vars = {}

        self.create_layout()
        self.show_books_page() 

    def create_layout(self):
        """
        Thiết lập bố cục khung (grid) cho toàn bộ ứng dụng.

        Chia cửa sổ thành hai phần chính:
        - Sidebar: Chứa logo và các nút điều hướng trang.
        - Content: Khung chứa động để hiển thị nội dung của từng tính năng.
        """
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="Library Manager", font=("Segoe UI", 22, "bold"), text_color="#1a73e8").pack(pady=(30, 40))

        menus = [
            ("📚 Kho Sách", self.show_books_page),
            ("👥 Độc Giả", self.show_readers_page),
            ("➕ Thêm Sách", self.show_add_book_page),
            ("👤 Thêm Độc Giả", self.show_add_reader_page),
            ("📤 Mượn Sách", self.show_borrow_page),
            ("📥 Trả Sách", self.show_return_page),
            ("⚙️ Cài Đặt", self.show_settings_page)
        ]

        for text, command in menus:
            ctk.CTkButton(self.sidebar, text=text, command=command, anchor="w", height=45, 
                          fg_color="transparent", text_color=("gray10", "gray90"),
                          hover_color=("#ebebeb", "#323232")).pack(fill="x", padx=15, pady=5)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)

    def clear_content(self):
        """
        Xóa sạch tất cả các widget hiện có trong khung nội dung (self.content).

        Phương thức này được gọi mỗi khi người dùng chuyển trang để chuẩn bị 
        không gian trống cho trang mới.
        """
        for widget in self.content.winfo_children():
            widget.destroy()

    def create_header(self, title):
        """
        Tạo và hiển thị tiêu đề lớn cho trang hiện tại.

        Args:
            title (str): Nội dung tiêu đề cần hiển thị (ví dụ: "Quản Lý Kho Sách").
        """
        self.title_lbl = ctk.CTkLabel(self.content, text=title, font=("Segoe UI", 28, "bold"))
        self.title_lbl.pack(anchor="w", pady=(0, 20))


    def show_books_page(self):
        """"
        Hiển thị trang quản lý kho sách.

        Trang này bao gồm:
        - Thanh tìm kiếm thời gian thực.
        - Bảng dữ liệu (Treeview) hiển thị ID, tên sách, tác giả và trạng thái.
        """
        self.clear_content()
        self.create_header("Quản Lý Kho Sách")
        
        self.search_entry = ctk.CTkEntry(self.content, placeholder_text="Tìm tên sách hoặc tác giả...", width=400, height=35)
        self.search_entry.pack(anchor="w", pady=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.search_event)

        self.tree_frame = ctk.CTkFrame(self.content)
        self.tree_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("id", "title", "author", "status"), show="headings")
        for c, h in zip(self.tree["columns"], ["ID", "Tên Sách", "Tác Giả", "Trạng Thái"]):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=150, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        self.refresh_books()

    def show_readers_page(self):
        """
        Hiển thị trang danh sách độc giả.

        Trang này hiển thị bảng thông tin về các độc giả đã đăng ký 
        và số lượng sách họ đang mượn.
        """
        self.clear_content()
        self.create_header("Danh Sách Độc Giả")

        self.search_entry = ctk.CTkEntry(self.content, placeholder_text="Tìm tên hoặc mã độc giả...", width=400, height=35)
        self.search_entry.pack(anchor="w", pady=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.search_event)

        self.tree_frame = ctk.CTkFrame(self.content)
        self.tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("id", "name", "borrowed"), show="headings")
        for c, h in zip(self.tree["columns"], ["ID Độc Giả", "Họ Tên", "Sách Đang Giữ"]):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=200, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        self.refresh_readers()

    def search_event(self, event=None):
        """
        Xử lý sự kiện tìm kiếm khi người dùng nhập dữ liệu vào ô Search.

        Dựa trên tiêu đề trang hiện tại, hàm sẽ gọi phương thức tìm kiếm tương ứng 
        trong LibraryManager và cập nhật lại bảng dữ liệu (Treeview).

        Args:
            event (optional): Sự kiện phím bấm từ bàn phím.
        """
        kw = self.search_entry.get().strip()
        current_page = self.title_lbl.cget("text")
        for i in self.tree.get_children(): self.tree.delete(i)

        if current_page == "Quản Lý Kho Sách":
            results = self.manager.search_books(kw)
            for b in results:
                status = "🔴 Đã mượn" if b.is_borrowed else "🟢 Sẵn có"
                self.tree.insert("", "end", values=(b.book_id, b.title, b.author, status))
        elif current_page == "Danh Sách Độc Giả":
            results = self.manager.search_readers(kw)
            for r in results:
                self.tree.insert("", "end", values=(r.reader_id, r.name, f"{r.currently_borrowed}/{r.max_books}"))

    def refresh_books(self):
        """Tải lại toàn bộ danh sách sách từ LibraryManager lên bảng hiển thị."""
        for i in self.tree.get_children(): self.tree.delete(i)
        for b in self.manager.books.values():
            status = "🔴 Đã mượn" if b.is_borrowed else "🟢 Sẵn có"
            self.tree.insert("", "end", values=(b.book_id, b.title, b.author, status))

    def refresh_readers(self):
        """Tải lại toàn bộ danh sách độc giả từ LibraryManager lên bảng hiển thị."""
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.manager.readers.values():
            self.tree.insert("", "end", values=(r.reader_id, r.name, f"{r.currently_borrowed}/{r.max_books}"))


    def show_add_book_page(self):
        """
        Hiển thị form nhập liệu để thêm sách mới vào kho.

        Bao gồm các trường nhập: ID, Tên, Tác giả, Thể loại và nút lưu dữ liệu.
        """
        self.clear_content()
        self.create_header("Thêm Sách Mới")
        
        form = ctk.CTkFrame(self.content, fg_color="transparent")
        form.pack(pady=20, anchor="w")

        fields = ["Mã Sách (ID)", "Tên Sách", "Tác Giả", "Thể Loại"]
        entries = {}
        for f in fields:
            ctk.CTkLabel(form, text=f, font=("Segoe UI", 14)).pack(anchor="w", pady=(10, 2))
            e = ctk.CTkEntry(form, width=400, height=35)
            e.pack(anchor="w", pady=5)
            entries[f] = e

        def save():
            if not entries["Mã Sách (ID)"].get() or not entries["Tên Sách"].get():
                messagebox.showwarning("Lỗi", "Vui lòng nhập ID và Tên sách!")
                return
            self.manager.add_book(entries["Mã Sách (ID)"].get(), entries["Tên Sách"].get(), 
                                  entries["Tác Giả"].get(), entries["Thể Loại"].get())
            messagebox.showinfo("Thành công", "Đã thêm sách vào kho.")
            self.show_books_page()

        ctk.CTkButton(self.content, text="Lưu Thông Tin", command=save, width=200, height=40, fg_color="#1e8e3e").pack(anchor="w", pady=20)

    def show_add_reader_page(self):
        """
        Hiển thị form đăng ký độc giả mới.

        Yêu cầu các thông tin: ID độc giả, Họ tên và Số điện thoại.
        """
        self.clear_content()
        self.create_header("Đăng Ký Độc Giả")

        form = ctk.CTkFrame(self.content, fg_color="transparent")
        form.pack(pady=20, anchor="w")

        ctk.CTkLabel(form, text="Mã Độc Giả (ID)").pack(anchor="w", pady=(10, 2))
        e_id = ctk.CTkEntry(form, width=400, height=35); e_id.pack(pady=5)
        
        ctk.CTkLabel(form, text="Họ và Tên").pack(anchor="w", pady=(10, 2))
        e_name = ctk.CTkEntry(form, width=400, height=35); e_name.pack(pady=5)

        ctk.CTkLabel(form, text="Số Điện Thoại").pack(anchor="w", pady=(10, 2))
        e_phone = ctk.CTkEntry(form, width=400, height=35); e_phone.pack(pady=5)

        def save():
            self.manager.add_reader(e_id.get(), e_name.get(), e_phone.get())
            messagebox.showinfo("Thành công", "Đã đăng ký độc giả mới.")
            self.show_readers_page()

        ctk.CTkButton(self.content, text="Xác Nhận Đăng Ký", command=save, width=200, height=40).pack(anchor="w", pady=20)

    def show_borrow_page(self):
        """
        Hiển thị giao diện cho phép mượn nhiều cuốn sách cùng lúc.

        Người dùng nhập ID độc giả và danh sách mã sách (cách nhau bởi dấu phẩy).
        """
        self.clear_content()
        self.create_header("Mượn Nhiều Sách")

        ctk.CTkLabel(self.content, text="ID Độc Giả:").pack(anchor="w", pady=(10, 2))
        e_r = ctk.CTkEntry(self.content, width=400, height=35); e_r.pack(anchor="w", pady=5)

        ctk.CTkLabel(self.content, text="ID Sách (Nhập nhiều mã, cách nhau bằng dấu phẩy):").pack(anchor="w", pady=(15, 2))
        e_b = ctk.CTkTextbox(self.content, width=500, height=150); e_b.pack(anchor="w", pady=5)

        def go():
            r_id = e_r.get().strip()
            b_ids = [i.strip() for i in e_b.get("1.0", "end").strip().split(",") if i.strip()]
            if not r_id or not b_ids:
                messagebox.showwarning("Lỗi", "Hãy nhập đủ mã độc giả và mã sách!")
                return
            msg = self.manager.borrow_multiple_books(r_id, b_ids)
            messagebox.showinfo("Kết quả", msg)
            self.show_books_page()

        ctk.CTkButton(self.content, text="Thực Hiện Mượn", command=go, width=200, height=40, fg_color="#1a73e8").pack(anchor="w", pady=20)

    def show_return_page(self):
        """
        Hiển thị giao diện trả sách thông minh.

        Quy trình:
        1. Nhập mã độc giả và nhấn "Kiểm Tra".
        2. Hệ thống liệt kê các sách độc giả đang mượn dưới dạng Checkbox.
        3. Người dùng chọn sách muốn trả và nhấn "Xác Nhận".
        """
        self.clear_content()
        self.create_header("Trả Nhiều Sách")

        search_row = ctk.CTkFrame(self.content, fg_color="transparent")
        search_row.pack(anchor="w", pady=10)

        ctk.CTkLabel(search_row, text="Nhập mã Độc giả: ").pack(side="left")
        e_r = ctk.CTkEntry(search_row, width=250); e_r.pack(side="left", padx=10)
        
        scroll_frame = ctk.CTkScrollableFrame(self.content, width=600, height=300, label_text="Danh sách sách đang mượn")
        scroll_frame.pack(anchor="w", pady=10)

        def find():
            for child in scroll_frame.winfo_children(): child.destroy()
            self.return_check_vars.clear()
            r_id = e_r.get().strip()
            target_books = [b for b in self.manager.books.values() if b.borrower_id == r_id]
            
            if not target_books:
                ctk.CTkLabel(scroll_frame, text="Không tìm thấy sách nào đang mượn.").pack(pady=10)
                return

            for b in target_books:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(scroll_frame, text=f"{b.title} (ID: {b.book_id})", variable=var)
                cb.pack(anchor="w", pady=5)
                self.return_check_vars[b.book_id] = var

        ctk.CTkButton(search_row, text="Kiểm Tra", command=find, width=100).pack(side="left")

        def ok():
            selected_ids = [b_id for b_id, var in self.return_check_vars.items() if var.get()]
            if not selected_ids:
                messagebox.showwarning("Chú ý", "Hãy chọn ít nhất một cuốn sách để trả!")
                return
            r_id = e_r.get().strip()
            titles, fine = self.manager.return_multiple_books(r_id, selected_ids)
            messagebox.showinfo("Kết quả", f"Đã trả: {', '.join(titles)}\nTổng phạt: {fine:,.0f} VNĐ")
            self.show_books_page()

        ctk.CTkButton(self.content, text="Xác Nhận Trả Sách", command=ok, width=200, height=40, fg_color="#1e8e3e").pack(anchor="w", pady=15)

    def show_settings_page(self):
        """
        Hiển thị trang cấu hình hệ thống.

        Cho phép quản trị viên thay đổi giới hạn mượn sách và đơn giá phạt 
        trên mỗi ngày quá hạn.
        """
        self.clear_content()
        self.create_header("Cài Đặt Hệ Thống")

        ctk.CTkLabel(self.content, text="Giới hạn mượn (cuốn):").pack(anchor="w", pady=(10, 2))
        e_m = ctk.CTkEntry(self.content, width=200)
        e_m.insert(0, str(self.manager.settings["max_books"]))
        e_m.pack(anchor="w", pady=5)
        
        ctk.CTkLabel(self.content, text="Tiền phạt mỗi ngày quá hạn (VNĐ):").pack(anchor="w", pady=(10, 2))
        e_f = ctk.CTkEntry(self.content, width=200)
        e_f.insert(0, str(self.manager.settings["fine_per_day"]))
        e_f.pack(anchor="w", pady=5)

        def save():
            try:
                max_b = int(e_m.get() or 5)
                fine = int(e_f.get() or 5000)
                self.manager.update_settings(max_b, fine)
                messagebox.showinfo("Cài đặt", "Đã cập nhật hệ thống thành công.")
                self.show_books_page()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

        ctk.CTkButton(self.content, text="Lưu Cấu Hình", command=save, width=200, height=40).pack(anchor="w", pady=20)