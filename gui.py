import customtkinter as ctk
from tkinter import ttk, messagebox
from library_manager import LibraryManager

class LibraryGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("THƯ VIỆN PRO v5.5")
        self.geometry("1100x700")
        self.manager = LibraryManager()
        self.create_layout()
        self.show_books_page()

    def create_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="Library Manager", font=("Segoe UI", 22, "bold"), text_color="#1a73e8").pack(pady=(30, 40))

        menus = [
            ("📚 Kho Sách", self.show_books_page), ("👥 Độc Giả", self.show_readers_page),
            ("➕ Thêm Sách", self.open_add_book_win), ("👤 Thêm Độc Giả", self.open_add_reader_win),
            ("📤 Mượn Sách", self.open_borrow_win), ("📥 Trả Sách", self.open_return_win),
            ("⚙️ Cài Đặt", self.open_settings_win)
        ]

        for text, command in menus:
            ctk.CTkButton(self.sidebar, text=text, command=command, anchor="w", height=45, fg_color="transparent", text_color=("gray10", "gray90")).pack(fill="x", padx=15, pady=5)

        # Main Content
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        
        self.title_lbl = ctk.CTkLabel(self.content, text="", font=("Segoe UI", 28, "bold"))
        self.title_lbl.pack(anchor="w", pady=(0, 10))

        # Search Bar
        self.search_entry = ctk.CTkEntry(self.content, placeholder_text="Tìm kiếm nhanh...", width=400, height=35)
        self.search_entry.pack(anchor="w", pady=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.search_event)

        # Table
        self.tree_frame = ctk.CTkFrame(self.content)
        self.tree_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scroller = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scroller.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroller.set)

    def search_event(self, event=None):
        kw = self.search_entry.get().strip()
        current_page = self.title_lbl.cget("text")

        # Xóa trắng bảng hiện tại trước khi hiển thị kết quả tìm kiếm
        for i in self.tree.get_children():
            self.tree.delete(i)

        if current_page == "Quản Lý Kho Sách":
            # Logic tìm kiếm Sách
            results = self.manager.search_books(kw)
            for b in results:
                status = "🔴 Đã mượn" if b.is_borrowed else "🟢 Sẵn có"
                self.tree.insert("", "end", values=(b.book_id, b.title, b.author, status))

        elif current_page == "Danh Sách Độc Giả":
            # Logic tìm kiếm Độc giả
            results = self.manager.search_readers(kw)
            for r in results:
                self.tree.insert("", "end", values=(r.reader_id, r.name, f"{r.currently_borrowed}/{r.max_books}"))
    
    def show_books_page(self):
        self.search_entry.delete(0, 'end')
        self.title_lbl.configure(text="Quản Lý Kho Sách")
        self.search_entry.configure(placeholder_text="Tìm tên sách hoặc tác giả...")
        self.tree["columns"] = ("id", "title", "author", "status")
        for c, h in zip(self.tree["columns"], ["ID", "Tên Sách", "Tác Giả", "Trạng Thái"]):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=150, anchor="center")
        self.refresh_books()

    def refresh_books(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for b in self.manager.books.values():
            status = "🔴 Đã mượn" if b.is_borrowed else "🟢 Sẵn có"
            self.tree.insert("", "end", values=(b.book_id, b.title, b.author, status))

    def show_readers_page(self):
        self.search_entry.delete(0, 'end')
        self.title_lbl.configure(text="Danh Sách Độc Giả")
        self.search_entry.configure(placeholder_text="Tìm tên hoặc mã độc giả...")
        self.tree["columns"] = ("id", "name", "borrowed")
        for c, h in zip(self.tree["columns"], ["ID Độc Giả", "Họ Tên", "Sách Đang Giữ"]):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=200, anchor="center")
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.manager.readers.values():
            self.tree.insert("", "end", values=(r.reader_id, r.name, f"{r.currently_borrowed}/{r.max_books}"))

    def open_add_book_win(self):
        win = ctk.CTkToplevel(self)
        win.title("Thêm Sách")
        win.geometry("350x400")
        win.attributes("-topmost", True)

        fields = ["ID", "Tên", "Tác giả", "Thể loại"]
        ents = {}
        for f in fields: 
            ctk.CTkLabel(win, text=f).pack(pady=(5, 0))
            e = ctk.CTkEntry(win, width=250); e.pack(pady=5)
            ents[f] = e

        def save():
            if not ents["ID"].get() or not ents["Tên"].get():
                messagebox.showwarning("Lỗi", "Vui lòng nhập ID và Tên")
                return
            self.manager.add_book(ents["ID"].get(), ents["Tên"].get(), ents["Tác giả"].get(), ents["Thể loại"].get())
            self.refresh_books()
            win.destroy()
        ctk.CTkButton(win, text="Lưu", command=save, fg_color="#1e8e3e").pack(pady=20)

    # ... (Các hàm open_add_reader_win, open_borrow_win giữ nguyên logic popup của bạn)
    
    def open_add_reader_win(self):
        win = ctk.CTkToplevel(self)
        win.title("Thêm Độc Giả")
        win.geometry("350x350")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="ID Độc Giả").pack(pady=(10, 0))
        e_id = ctk.CTkEntry(win, width=250); e_id.pack(pady=5)
        ctk.CTkLabel(win, text="Họ Tên").pack(pady=(10, 0))
        e_n = ctk.CTkEntry(win, width=250); e_n.pack(pady=5)
        ctk.CTkLabel(win, text="Số Điện Thoại").pack(pady=(10, 0))
        e_p = ctk.CTkEntry(win, width=250); e_p.pack(pady=5)

        def save():
            self.manager.add_reader(e_id.get(), e_n.get(), e_p.get())
            self.show_readers_page()
            win.destroy()
        ctk.CTkButton(win, text="Đăng Ký", command=save).pack(pady=20)

    def open_borrow_win(self):
        win = ctk.CTkToplevel(self)
        win.title("Mượn Sách")
        win.geometry("300x250")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="ID Độc Giả").pack(pady=5)
        e_r = ctk.CTkEntry(win); e_r.pack()
        ctk.CTkLabel(win, text="ID Sách").pack(pady=5)
        e_b = ctk.CTkEntry(win); e_b.pack()

        def go():
            msg = self.manager.borrow_book(e_r.get(), e_b.get())
            messagebox.showinfo("Thông báo", msg)
            self.refresh_books()
            win.destroy()
        ctk.CTkButton(win, text="Xác nhận", command=go).pack(pady=20)

    def open_return_win(self):
        win = ctk.CTkToplevel(self)
        win.title("Trả Sách")
        win.geometry("400x480")
        win.attributes("-topmost", True)
        
        ctk.CTkLabel(win, text="Nhập mã Độc giả:").pack(pady=10)
        e_r = ctk.CTkEntry(win); e_r.pack()
        
        scroll_frame = ctk.CTkScrollableFrame(win, width=300, height=200)
        scroll_frame.pack(pady=10)
        selected_book = ctk.StringVar()

        def find():
            for child in scroll_frame.winfo_children(): child.destroy()
            target_books = [b for b in self.manager.books.values() if b.borrower_id == e_r.get()]
            for b in target_books:
                ctk.CTkRadioButton(scroll_frame, text=b.title, variable=selected_book, value=b.book_id).pack(anchor="w", pady=2)

        ctk.CTkButton(win, text="Tìm sách", command=find).pack()

        def ok():
            if not selected_book.get(): return
            fine = self.manager.return_book(e_r.get(), selected_book.get())
            messagebox.showinfo("Trả sách", f"Phí phạt: {fine}đ")
            self.refresh_books()
            win.destroy()
        ctk.CTkButton(win, text="Xác nhận trả", command=ok, fg_color="#1e8e3e").pack(pady=10)

    def open_settings_win(self):
        win = ctk.CTkToplevel(self)
        win.title("Cài Đặt")
        win.geometry("300x250")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="Giới hạn (cuốn):").pack()
        e_m = ctk.CTkEntry(win); e_m.insert(0, str(self.manager.settings["max_books"])); e_m.pack()
        ctk.CTkLabel(win, text="Phạt (đ/ngày):").pack()
        e_f = ctk.CTkEntry(win); e_f.insert(0, str(self.manager.settings["fine_per_day"])); e_f.pack()

        def save():
            self.manager.update_settings(int(e_m.get() or 5), int(e_f.get() or 5000))
            win.destroy()
        ctk.CTkButton(win, text="Lưu", command=save).pack(pady=10)