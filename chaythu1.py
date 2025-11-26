# ================================================
# ỨNG DỤNG QUẢN LÝ CÁC TUYẾN DU LỊCH
# Python + Tkinter + MySQL
# Đã sửa hết lỗi thường gặp khi chạy trên VS Code
# ================================================

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from datetime import date
import sys

# ==================== KẾT NỐI MySQL ====================
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",           # ← Thay nếu em dùng user khác
            password="",           # ← Điền mật khẩu MySQL nếu có
            database="qltuyen_dulich",
            charset='utf8mb4'
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi kết nối CSDL", f"Không thể kết nối MySQL!\n{err}")
        sys.exit()

# ==================== CANH GIỮA CỬA SỔ ====================
def center_window(win, w=1000, h=650):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ==================== TẠO CỬA SỔ CHÍNH ====================
root = tk.Tk()
root.title("QUẢN LÝ CÁC TUYẾN DU LỊCH")
root.iconbitmap(default='')  # tránh lỗi icon trên một số máy
center_window(root, 1000, 650)
root.resizable(False, False)

# Tiêu đề lớn
lbl_title = tk.Label(root, text="QUẢN LÝ CÁC TUYẾN DU LỊCH", font=("Times New Roman", 22, "bold"), fg="navy")
lbl_title.pack(pady=15)

# ==================== FRAME NHẬP LIỆU ====================
frame_input = tk.LabelFrame(root, text=" Thông tin tuyến du lịch ", font=("Times New Roman", 12, "bold"))
frame_input.pack(padx=20, pady=10, fill="x")

# Dòng 1
tk.Label(frame_input, text="Mã tuyến:", font=("Times New Roman", 11)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
entry_matuyen = tk.Entry(frame_input, width=12, font=("Times New Roman", 11))
entry_matuyen.grid(row=0, column=1, padx=10, pady=8)

tk.Label(frame_input, text="Tên tuyến:", font=("Times New Roman", 11)).grid(row=0, column=2, padx=10, pady=8, sticky="w")
entry_tentuyen = tk.Entry(frame_input, width=35, font=("Times New Roman", 11))
entry_tentuyen.grid(row=0, column=3, padx=10, pady=8)

tk.Label(frame_input, text="Điểm xuất phát:", font=("Times New Roman", 11)).grid(row=0, column=4, padx=10, pady=8, sticky="w")
entry_xuatphat = tk.Entry(frame_input, width=20, font=("Times New Roman", 11))
entry_xuatphat.grid(row=0, column=5, padx=10, pady=8)

# Dòng 2
tk.Label(frame_input, text="Điểm đến:", font=("Times New Roman", 11)).grid(row=1, column=0, padx=10, pady=8, sticky="w")
entry_diemden = tk.Entry(frame_input, width=20, font=("Times New Roman", 11))
entry_diemden.grid(row=1, column=1, padx=10, pady=8)

tk.Label(frame_input, text="Ngày khởi hành:", font=("Times New Roman", 11)).grid(row=1, column=2, padx=10, pady=8, sticky="w")
date_khoihanh = DateEntry(frame_input, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd', font=("Times New Roman", 11))
date_khoihanh.grid(row=1, column=3, padx=10, pady=8)
date_khoihanh.set_date(date.today())

tk.Label(frame_input, text="Số ngày:", font=("Times New Roman", 11)).grid(row=1, column=4, padx=10, pady=8, sticky="w")
entry_songay = tk.Entry(frame_input, width=8, font=("Times New Roman", 11))
entry_songay.grid(row=1, column=5, padx=10, pady=8)

# Dòng 3
tk.Label(frame_input, text="Giá tour (VNĐ):", font=("Times New Roman", 11)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
entry_giatour = tk.Entry(frame_input, width=18, font=("Times New Roman", 11))
entry_giatour.grid(row=2, column=1, padx=10, pady=8)

tk.Label(frame_input, text="Số chỗ tối đa:", font=("Times New Roman", 11)).grid(row=2, column=2, padx=10, pady=8, sticky="w")
entry_socho = tk.Entry(frame_input, width=10, font=("Times New Roman", 11))
entry_socho.grid(row=2, column=3, padx=10, pady=8)

tk.Label(frame_input, text="Tìm kiếm:", font=("Times New Roman", 11)).grid(row=2, column=4, padx=10, pady=8, sticky="w")
entry_timkiem = tk.Entry(frame_input, width=25, font=("Times New Roman", 11))
entry_timkiem.grid(row=2, column=5, padx=10, pady=8)

# ==================== BẢNG DANH SÁCH ====================
tk.Label(root, text="Danh sách các tuyến du lịch", font=("Times New Roman", 14, "bold")).pack(anchor="w", padx=20, pady=(10,5))

columns = ("matuyen", "tentuyen", "xuatphat", "diemden", "ngaykh", "songay", "giatour", "socho")
tree = ttk.Treeview(root, columns=columns, show="headings", height=16)
tree.pack(padx=20, pady=5, fill="both", expand=True)

# Tiêu đề cột
tree.heading("matuyen", text="Mã tuyến")
tree.heading("tentuyen", text="Tên tuyến")
tree.heading("xuatphat", text="Xuất phát")
tree.heading("diemden", text="Điểm đến")
tree.heading("ngaykh", text="Ngày KH")
tree.heading("songay", text="Số ngày")
tree.heading("giatour", text="Giá tour")
tree.heading("socho", text="Số chỗ")

# Độ rộng cột
tree.column("matuyen", width=80, anchor="center")
tree.column("tentuyen", width=250)
tree.column("xuatphat", width=120)
tree.column("diemden", width=120)
tree.column("ngaykh", width=100, anchor="center")
tree.column("songay", width=80, anchor="center")
tree.column("giatour", width=130, anchor="center")
tree.column("socho", width=80, anchor="center")

# Thanh cuộn
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# ==================== CÁC HÀM CHỨC NĂNG ====================
def clear_input():
    for widget in [entry_matuyen, entry_tentuyen, entry_xuatphat, entry_diemden, entry_songay, entry_giatour, entry_socho]:
        widget.delete(0, tk.END)
    date_khoihanh.set_date(date.today())
    entry_timkiem.delete(0, tk.END)

def load_data(sql="SELECT * FROM tuyen_dulich"):
    for item in tree.get_children():
        tree.delete(item)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            row = list(row)
            row[6] = f"{int(row[6]):,}".replace(",", ".") + " đ"
            tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def them():
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = """INSERT INTO tuyen_dulich VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        val = (
            entry_matuyen.get(),
            entry_tentuyen.get(),
            entry_xuatphat.get(),
            entry_diemden.get(),
            date_khoihanh.get_date(),
            entry_songay.get(),
            entry_giatour.get().replace(".", ""),
            entry_socho.get()
        )
        cur.execute(sql, val)
        conn.commit()
        conn.close()
        load_data()
        clear_input()
        messagebox.showinfo("Thành công", "Thêm tuyến du lịch thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xoa():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn tuyến để xóa!")
        return
    if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa tuyến này?"):
        matuyen = tree.item(selected[0])["values"][0]
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM tuyen_dulich WHERE matuyen=%s", (matuyen,))
        conn.commit()
        conn.close()
        load_data()

def sua():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn tuyến để sửa!")
        return
    values = tree.item(selected[0])["values"]
    entry_matuyen.delete(0, tk.END); entry_matuyen.insert(0, values[0])
    entry_tentuyen.delete(0, tk.END); entry_tentuyen.insert(0, values[1])
    entry_xuatphat.delete(0, tk.END); entry_xuatphat.insert(0, values[2])
    entry_diemden.delete(0, tk.END); entry_diemden.insert(0, values[3])
    date_khoihanh.set_date(values[4])
    entry_songay.delete(0, tk.END); entry_songay.insert(0, values[5])
    entry_giatour.delete(0, tk.END); entry_giatour.insert(0, values[6].replace(" đ","").replace(".",""))
    entry_socho.delete(0, tk.END); entry_socho.insert(0, values[7])

def luu():
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql = """UPDATE tuyen_dulich SET tentuyen=%s, diemxuatphat=%s, diemden=%s,
                 ngaykhoihanh=%s, songay=%s, giatour=%s, sochotoida=%s WHERE matuyen=%s"""
        val = (
            entry_tentuyen.get(), entry_xuatphat.get(), entry_diemden.get(),
            date_khoihanh.get_date(), entry_songay.get(),
            entry_giatour.get().replace(".", ""), entry_socho.get(),
            entry_matuyen.get()
        )
        cur.execute(sql, val)
        conn.commit()
        conn.close()
        load_data()
        clear_input()
        messagebox.showinfo("Thành công", "Cập nhật thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def timkiem(event=None):
    keyword = entry_timkiem.get().strip()
    if keyword == "":
        load_data()
    else:
        sql = f"SELECT * FROM tuyen_dulich WHERE matuyen LIKE '%{keyword}%' OR tentuyen LIKE '%{keyword}%'"
        load_data(sql)

entry_timkiem.bind("<KeyRelease>", timkiem)

# ==================== NÚT CHỨC NĂNG ====================
frame_btn = tk.Frame(root)
frame_btn.pack(pady=15)

tk.Button(frame_btn, text="Thêm", width=10, bg="green", fg="white", font=("Times New Roman", 11, "bold"), command=them).grid(row=0, column=0, padx=8)
tk.Button(frame_btn, text="Lưu", width=10, bg="blue", fg="white", font=("Times New Roman", 11, "bold"), command=luu).grid(row=0, column=1, padx=8)
tk.Button(frame_btn, text="Sửa", width=10, bg="orange", fg="white", font=("Times New Roman", 11, "bold"), command=sua).grid(row=0, column=2, padx=8)
tk.Button(frame_btn, text="Hủy", width=10, font=("Times New Roman", 11, "bold"), command=clear_input).grid(row=0, column=3, padx=8)
tk.Button(frame_btn, text="Xóa", width=10, bg="red", fg="white", font=("Times New Roman", 11, "bold"), command=xoa).grid(row=0, column=4, padx=8)
tk.Button(frame_btn, text="Thoát", width=10, bg="gray", fg="white", font=("Times New Roman", 11, "bold"), command=root.quit).grid(row=0, column=5, padx=8)

# ==================== TẠO CSDL + BẢNG (nếu chưa có) ====================
try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS qltuyen_dulich CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("USE qltuyen_dulich")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tuyen_dulich (
        matuyen VARCHAR(10) PRIMARY KEY,
        tentuyen VARCHAR(200),
        diemxuatphat VARCHAR(100),
        diemden VARCHAR(100),
        ngaykhoihanh DATE,
        songay INT,
        giatour DECIMAL(15,0),
        sochotoida INT
    )""")
    conn.close()
except:
    pass

# Load dữ liệu lần đầu
load_data()

root.mainloop()