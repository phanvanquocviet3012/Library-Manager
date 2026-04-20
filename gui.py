import tkinter as tk
from tkinter import ttk, messagebox
from library_manager import LibraryManager

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("THƯ VIỆN PRO v5.5")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f2f5")
        self.manager = LibraryManager()
        self.colors = {"primary": "#1a73e8", "sidebar": "#ffffff", "success": "#1e8e3e"}
        self.create_layout()
        self.show_books_page()

    def create_layout(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=240, highlightthickness=1, highlightbackground="#dadce0")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="Library Manager", font=("Segoe UI", 16, "bold"), bg=self.colors["sidebar"], fg=self.colors["primary"], pady=30).pack()

        menus = [("📚 Kho Sách", self.show_books_page), ("👥 Độc Giả", self.show_readers_page),
                 ("➕ Thêm Sách", self.open_add_book_win), ("👤 Thêm Độc Giả", self.open_add_reader_win),
                 ("📤 Mượn Sách", self.open_borrow_win), ("📥 Trả Sách", self.open_return_win),
                 ("⚙️ Cài Đặt", self.open_settings_win)]

        for t, c in menus:
            btn = tk.Button(sidebar, text=t, command=c, font=("Segoe UI", 11), bg="white", fg="#5f6368", relief="flat", padx=20, pady=12, anchor="w", cursor="hand2")
            btn.pack(fill="x")

        # Main Content
        self.content = tk.Frame(self.root, bg="#f0f2f5", padx=30, pady=20)
        self.content.pack(side="right", fill="both", expand=True)
        self.title_lbl = tk.Label(self.content, text="", font=("Segoe UI", 18, "bold"), bg="#f0f2f5")
        self.title_lbl.pack(anchor="w", pady=(0, 20))

        self.tree = ttk.Treeview(self.content, show="headings")
        self.tree.pack(fill="both", expand=True)

    def show_books_page(self):
        self.title_lbl.config(text="Quản Lý Kho Sách")
        self.tree["columns"] = ("id", "title", "author", "status")
        for c, h in zip(self.tree["columns"], ["ID", "Tên Sách", "Tác Giả", "Trạng Thái"]):
            self.tree.heading(c, text=h); self.tree.column(c, width=150)
        self.refresh_books()

    def refresh_books(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for b in self.manager.books.values():
            s = "Đã mượn" if b.is_borrowed else "Sẵn có"
            self.tree.insert("", "end", values=(b.book_id, b.title, b.author, s))

    def show_readers_page(self):
        self.title_lbl.config(text="Danh Sách Độc Giả")
        self.tree["columns"] = ("id", "name", "borrowed")
        for c, h in zip(self.tree["columns"], ["ID Độc Giả", "Họ Tên", "Sách Đang Giữ"]):
            self.tree.heading(c, text=h); self.tree.column(c, width=200)
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.manager.readers.values():
            self.tree.insert("", "end", values=(r.reader_id, r.name, f"{r.currently_borrowed}/{r.max_books}"))

    def open_add_book_win(self):
        win = tk.Toplevel(self.root); win.geometry("350x400")
        fields = ["ID", "Tên", "Tác giả", "Thể loại"]; ents = {}
        for f in fields: tk.Label(win, text=f).pack(); e = tk.Entry(win); e.pack(pady=5); ents[f] = e
        def save():
            self.manager.add_book(ents["ID"].get(), ents["Tên"].get(), ents["Tác giả"].get(), ents["Thể loại"].get())
            self.refresh_books(); win.destroy()
        tk.Button(win, text="Lưu", command=save, bg=self.colors["success"], fg="white").pack(pady=20)

    def open_add_reader_win(self):
        win = tk.Toplevel(self.root); win.geometry("350x300")
        tk.Label(win, text="ID").pack(); e_id = tk.Entry(win); e_id.pack()
        tk.Label(win, text="Tên").pack(); e_n = tk.Entry(win); e_n.pack()
        tk.Label(win, text="SĐT").pack(); e_p = tk.Entry(win); e_p.pack()
        def save():
            self.manager.add_reader(e_id.get(), e_n.get(), e_p.get())
            if self.title_lbl["text"] == "Danh Sách Độc Giả": self.show_readers_page()
            win.destroy()
        tk.Button(win, text="Đăng ký", command=save, bg=self.colors["primary"], fg="white").pack(pady=20)

    def open_borrow_win(self):
        win = tk.Toplevel(self.root); win.geometry("300x200")
        tk.Label(win, text="Mã Độc Giả:").pack(); e_r = tk.Entry(win); e_r.pack()
        tk.Label(win, text="Mã Sách:").pack(); e_b = tk.Entry(win); e_b.pack()
        def go(): messagebox.showinfo("Kết quả", self.manager.borrow_book(e_r.get(), e_b.get())); self.refresh_books(); win.destroy()
        tk.Button(win, text="Xác nhận", command=go).pack(pady=20)

    def open_return_win(self):
        win = tk.Toplevel(self.root); win.geometry("400x450")
        tk.Label(win, text="Nhập mã Độc giả:").pack(); e_r = tk.Entry(win); e_r.pack()
        lb = tk.Listbox(win, width=40); lb.pack(pady=10)
        def find():
            lb.delete(0, tk.END); win.target = [b for b in self.manager.books.values() if b.borrower_id == e_r.get()]
            for b in win.target: lb.insert(tk.END, b.title)
        tk.Button(win, text="Tìm sách", command=find).pack()
        def ok():
            sel = lb.curselection()
            if sel:
                fine = self.manager.return_book(e_r.get(), win.target[sel[0]].book_id)
                messagebox.showinfo("Trả sách", f"Đã trả. Phạt: {fine}đ"); self.refresh_books(); win.destroy()
        tk.Button(win, text="Xác nhận trả", bg=self.colors["success"], fg="white", command=ok).pack(pady=10)

    def open_settings_win(self):
        win = tk.Toplevel(self.root); win.geometry("300x200")
        tk.Label(win, text="Giới hạn mượn:").pack(); e_m = tk.Entry(win); e_m.insert(0, self.manager.settings["max_books"]); e_m.pack()
        tk.Label(win, text="Tiền phạt (đ/ngày):").pack(); e_f = tk.Entry(win); e_f.insert(0, self.manager.settings["fine_per_day"]); e_f.pack()
        def save(): messagebox.showinfo("Cài đặt", self.manager.update_settings(int(e_m.get()), int(e_f.get()))); win.destroy()
        tk.Button(win, text="Lưu", command=save).pack(pady=20)