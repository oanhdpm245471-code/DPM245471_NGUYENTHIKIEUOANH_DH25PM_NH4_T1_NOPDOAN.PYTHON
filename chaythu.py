import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from datetime import date

# ====== Kết nối CSDL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # thay đổi nếu cần
        password="",          # thay đổi nếu có mật khẩu
        database="qltuyen_dulich"
    )

# ====== Canh giữa cửa sổ ======
def center_window(win, w=900, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản Lý Các Tuyến Du Lịch")
center_window(root, 900, 600)
root.resizable(False, False)

# Tiêu đề
lbl_title = tk.Label(root, text="QUẢN LÝ CÁC TUYẾN DU LỊCH", font=("Arial", 20, "bold"), fg="blue")
lbl_title.pack(pady=15)

# Frame nhập liệu
frame_input = tk.Frame(root)
frame_input.pack(pady=10, padx=20, fill="x")

# Dòng 1
tk.Label(frame_input, text="Mã tuyến", font=("Arial", 11)).grid(row=0, column=0, padx=8, pady=8, sticky="w")
entry_matuyen = tk.Entry(frame_input, width=12, font=("Arial", 11))
entry_matuyen.grid(row=0, column=1, padx=8, pady=8)

tk.Label(frame_input, text="Tên tuyến", font=("Arial", 11)).grid(row=0, column=2, padx=8, pady=8, sticky="w")
entry_tentuyen = tk.Entry(frame_input, width=30, font=("Arial", 11))
entry_tentuyen.grid(row=0, column=3, padx=8, pady=8)

tk.Label(frame_input, text="Điểm xuất phát", font=("Arial", 11)).grid(row=0, column=4, padx=8, pady=8, sticky="w")
entry_xuatphat = tk.Entry(frame_input, width=20, font=("Arial", 11))
entry_xuatphat.grid(row=0, column=5, padx=8, pady=8)

# Dòng 2
tk.Label(frame_input, text="Điểm đến", font=("Arial", 11)).grid(row=1, column=0, padx=8, pady=8, sticky="w")
entry_diemden = tk.Entry(frame_input, width=20, font=("Arial", 11))
entry_diemden.grid(row=1, column=1, padx=8, pady=8)

tk.Label(frame_input, text="Ngày khởi hành", font=("Arial", 11)).grid(row=1, column=2, padx=8, pady=8, sticky="w")
date_khoihanh = DateEntry(frame_input, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
date_khoihanh.grid(row=1, column=3, padx=8, pady=8)

tk.Label(frame_input, text="Số ngày", font=("Arial", 11)).grid(row=1, column=4, padx=8, pady=8, sticky="w")
entry_songay = tk.Entry(frame_input, width=8, font=("Arial", 11))
entry_songay.grid(row=1, column=5, padx=8, pady=8)

# Dòng 3
tk.Label(frame_input, text="Giá tour (VNĐ)", font=("Arial", 11)).grid(row=2, column=0, padx=8, pady=8, sticky="w")
entry_giatour = tk.Entry(frame_input, width=15, font=("Arial", 11))
entry_giatour.grid(row=2, column=1, padx=8, pady=8)

tk.Label(frame_input, text="Số chỗ tối đa", font=("Arial", 11)).grid(row=2, column=2, padx=8, pady=8, sticky="w")
entry_socho = tk.Entry(frame_input, width=10, font=("Arial", 11))
entry_socho.grid(row=2, column=3, padx=8, pady=8)

# Tìm kiếm
tk.Label(frame_input, text="Tìm kiếm:", font=("Arial", 11)).grid(row=2, column=4, padx=8, pady=8, sticky="w")
entry_timkiem = tk.Entry(frame_input, width=25, font=("Arial", 11))
entry_timkiem.grid(row=2, column=5, padx=8, pady=8, sticky="w")

# Bảng danh sách
lbl_ds = tk.Label(root, text="Danh sách các tuyến du lịch", font=("Arial", 12, "bold"))
lbl_ds.pack(anchor="w", padx=20)

columns = ("matuyen", "tentuyen", "xuatphat", "diemden", "ngaykh", "songay", "giatour", "socho")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col.replace("matuyen","Mã tuyến").replace("tentuyen","Tên tuyến")
                        .replace("xuatphat","Xuất phát").replace("diemden","Điểm đến")
                        .replace("ngaykh","Ngày KH").replace("songay","Số ngày")
                        .replace("giatour","Giá tour").replace("socho","Chỗ"))
tree.column("matuyen", width=80, anchor="center")
tree.column("tentuyen", width=200)
tree.column("xuatphat", width=100)
tree.column("diemden", width=100)
tree.column("ngaykh", width=100, anchor="center")
tree.column("songay", width=70, anchor="center")
tree.column("giatour", width=110, anchor="center")
tree.column("socho", width=80, anchor="center")
tree.pack(padx=20, pady=10, fill="both", expand=True)

# ====== Chức năng ======
def clear_input():
    for entry in [entry_matuyen, entry_tentuyen, entry_xuatphat, entry_diemden, entry_songay, entry_giatour, entry_socho]:
        entry.delete(0, tk.END)
    date_khoihanh.set_date(date.today())
    entry_timkiem.delete(0, tk.END)

def load_data(query="SELECT * FROM tuyen_dulich"):
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(query)
    for row in cur.fetchall():
        row = list(row)
        row[6] = f"{int(row[6]):,}".replace(",",".") + " đ"
        tree.insert("", tk.END, values=row)
    conn.close()

def them():
    data = (
        entry_matuyen.get(), entry_tentuyen.get(), entry_xuatphat.get(),
        entry_diemden.get(), date_khoihanh.get_date(), entry_songay.get(),
        entry_giatour.get().replace(".",""), entry_socho.get()
    )
    if not all([data[0], data[1], data[4], data[5], data[6], data[7]]):
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc!")
        return
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO tuyen_dulich VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", data)
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
    matuyen = tree.item(selected[0])["values"][0]
    if messagebox.askyesno("Xác nhận", f"Xóa tuyến {matuyen}?"):
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
    matuyen = entry_matuyen.get()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE tuyen_dulich SET tentuyen=%s, diemxuatphat=%s, diemden=%s,
                   ngaykhoihanh=%s, songay=%s, giatour=%s, sochotoida=%s WHERE matuyen=%s""",
                (entry_tentuyen.get(), entry_xuatphat.get(), entry_diemden.get(),
                 date_khoihanh.get_date(), entry_songay.get(),
                 entry_giatour.get().replace(".",""), entry_socho.get(), matuyen))
    conn.commit()
    conn.close()
    load_data()
    clear_input()
    messagebox.showinfo("Thành công", "Cập nhật thành công!")

def timkiem(event=None):
    keyword = entry_timkiem.get().lower()
    query = f"SELECT * FROM tuyen_dulich WHERE LOWER(tentuyen) LIKE '%{keyword}%' OR matuyen LIKE '%{keyword}%'"
    load_data(query)

entry_timkiem.bind("<KeyRelease>", timkiem)

# Nút chức năng
frame_btn = tk.Frame(root)
frame_btn.pack(pady=12)

tk.Button(frame_btn, text="Thêm", width=10, bg="green", fg="white", font=("Arial", 10, "bold"), command=them).grid(row=0, column=0, padx=8)
tk.Button(frame_btn, text="Lưu", width=10, bg="blue", fg="white", font=("Arial", 10, "bold"), command=luu).grid(row=0, column=1, padx=8)
tk.Button(frame_btn, text="Sửa", width=10, bg="orange", fg="white", font=("Arial", 10, "bold"), command=sua).grid(row=0, column=2, padx=8)
tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=8)
tk.Button(frame_btn, text="Xóa", width=10, bg="red", fg="white", font=("Arial", 10, "bold"), command=xoa).grid(row=0, column=4, padx=8)
tk.Button(frame_btn, text="Thoát", width=10, bg="gray", fg="white", command=root.quit).grid(row=0, column=5, padx=8)

# Load dữ liệu ban đầu
load_data()
root.mainloop()