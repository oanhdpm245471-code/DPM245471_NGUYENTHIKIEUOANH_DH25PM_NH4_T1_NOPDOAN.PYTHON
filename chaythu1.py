import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Thay bằng user của em
        password="",          # Thay bằng password MySQL của em
        database="qltuyen_dulich"
    )

# ====== Căn giữa cửa sổ ======
def center_window(win, w=900, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("QUẢN LÝ TUYẾN DU LỊCH - CÔNG TY DU LỊCH ABC")
center_window(root, 900, 600)
root.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ TUYẾN DU LỊCH", font=("Arial", 20, "bold"), fg="blue")
lbl_title.pack(pady=15)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root)
frame_info.pack(pady=10, padx=20, fill="x")

# Dòng 1
tk.Label(frame_info, text="Mã tuyến", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
entry_matuyen = tk.Entry(frame_info, width=15, font=("Arial", 10))
entry_matuyen.grid(row=0, column=1, padx=10, pady=8, sticky="w")

tk.Label(frame_info, text="Tên tuyến", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=8, sticky="w")
entry_tentuyen = tk.Entry(frame_info, width=40, font=("Arial", 10))
entry_tentuyen.grid(row=0, column=3, padx=10, pady=8, sticky="w")

# Dòng 2
tk.Label(frame_info, text="Điểm đi", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=8, sticky="w")
entry_diemdi = tk.Entry(frame_info, width=20, font=("Arial", 10))
entry_diemdi.grid(row=1, column=1, padx=10, pady=8, sticky="w")

tk.Label(frame_info, text="Điểm đến", font=("Arial", 10)).grid(row=1, column=2, padx=10, pady=8, sticky="w")
entry_diemden = tk.Entry(frame_info, width=20, font=("Arial", 10))
entry_diemden.grid(row=1, column=3, padx=10, pady=8, sticky="w")

# Dòng 3
tk.Label(frame_info, text="Thời gian", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
entry_thoigian = tk.Entry(frame_info, width=20, font=("Arial", 10))
entry_thoigian.grid(row=2, column=1, padx=10, pady=8, sticky="w")

tk.Label(frame_info, text="Giá (VNĐ)", font=("Arial", 10)).grid(row=2, column=2, padx=10, pady=8, sticky="w")
entry_gia = tk.Entry(frame_info, width=20, font=("Arial", 10))
entry_gia.grid(row=2, column=3, padx=10, pady=8, sticky="w")

# Dòng 4 - Mô tả
tk.Label(frame_info, text="Mô tả", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=8, sticky="w")
entry_mota = tk.Text(frame_info, width=70, height=4, font=("Arial", 10))
entry_mota.grid(row=3, column=1, columnspan=3, padx=10, pady=8, sticky="w")

# ====== Bảng danh sách ======
lbl_ds = tk.Label(root, text="Danh sách tuyến du lịch", font=("Arial", 12, "bold"))
lbl_ds.pack(pady=10, anchor="w", padx=20)

columns = ("matuyen", "tentuyen", "diemdi", "diemden", "thoigian", "gia", "mota")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

# Tiêu đề cột
tree.heading("matuyen", text="Mã tuyến")
tree.heading("tentuyen", text="Tên tuyến")
tree.heading("diemdi", text="Điểm đi")
tree.heading("diemden", text="Điểm đến")
tree.heading("thoigian", text="Thời gian")
tree.heading("gia", text="Giá (VNĐ)")
tree.heading("mota", text="Mô tả")

# Độ rộng cột
tree.column("matuyen", width=80, anchor="center")
tree.column("tentuyen", width=200)
tree.column("diemdi", width=100)
tree.column("diemden", width=100)
tree.column("thoigian", width=100, anchor="center")
tree.column("gia", width=100, anchor="e")
tree.column("mota", width=200)

tree.pack(padx=20, pady=10, fill="both", expand=True)

# ====== Hàm chức năng ======
def clear_input():
    entry_matuyen.delete(0, tk.END)
    entry_tentuyen.delete(0, tk.END)
    entry_diemdi.delete(0, tk.END)
    entry_diemden.delete(0, tk.END)
    entry_thoigian.delete(0, tk.END)
    entry_gia.delete(0, tk.END)
    entry_mota.delete("1.0", tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tuyen_dulich")
        for row in cur.fetchall():
            # Format giá tiền có dấu chấm
            gia_format = "{:,.0f}".format(row[5]) if row[5] else ""
            row_display = (row[0], row[1], row[2], row[3], row[4], gia_format, row[6])
            tree.insert("", tk.END, values=row_display)
        conn.close()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không tải được dữ liệu: {e}")

def them_tuyen():
    matuyen = entry_matuyen.get().strip()
    tentuyen = entry_tentuyen.get().strip()
    diemdi = entry_diemdi.get().strip()
    diemden = entry_diemden.get().strip()
    thoigian = entry_thoigian.get().strip()
    gia = entry_gia.get().strip()
    mota = entry_mota.get("1.0", tk.END).strip()

    if not (matuyen and tentuyen and diemdi and diemden and gia):
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ các trường bắt buộc!")
        return

    try:
        gia_int = int(gia.replace(",", ""))
    except:
        messagebox.showerror("Lỗi", "Giá phải là số!")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO tuyen_dulich 
                       (matuyen, tentuyen, diemdi, diemden, thoigian, gia, mota) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (matuyen, tentuyen, diemdi, diemden, thoigian, gia_int, mota))
        conn.commit()
        conn.close()
        load_data()
        clear_input()
        messagebox.showinfo("Thành công", "Thêm tuyến du lịch thành công!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Lỗi", "Mã tuyến đã tồn tại!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xoa_tuyen():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn tuyến để xóa!")
        return
    matuyen = tree.item(selected)["values"][0]
    if messagebox.askyesno("Xác nhận", f"Xóa tuyến {matuyen}?"):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM tuyen_dulich WHERE matuyen=%s", (matuyen,))
            conn.commit()
            conn.close()
            load_data()
            messagebox.showinfo("Thành công", "Xóa thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

def chon_tuyen_de_sua(event):
    selected = tree.selection()
    if not selected:
        return
    values = tree.item(selected)["values"]
    clear_input()
    entry_matuyen.insert(0, values[0])
    entry_tentuyen.insert(0, values[1])
    entry_diemdi.insert(0, values[2])
    entry_diemden.insert(0, values[3])
    entry_thoigian.insert(0, values[4])
    entry_gia.insert(0, str(values[5]).replace(",", ""))
    entry_mota.insert("1.0", values[6])
    entry_matuyen.config(state="disabled")  # Không cho sửa mã tuyến

def luu_sua():
    matuyen = entry_matuyen.get().strip()
    if not matuyen:
        messagebox.showwarning("Lỗi", "Chưa chọn tuyến để sửa!")
        return
    tentuyen = entry_tentuyen.get().strip()
    diemdi = entry_diemdi.get().strip()
    diemden = entry_diemden.get().strip()
    thoigian = entry_thoigian.get().strip()
    gia = entry_gia.get().strip()
    mota = entry_mota.get("1.0", tk.END).strip()

    try:
        gia_int = int(gia.replace(",", ""))
    except:
        messagebox.showerror("Lỗi", "Giá phải là số!")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""UPDATE tuyen_dulich SET tentuyen=%s, diemdi=%s, diemden=%s, 
                       thoigian=%s, gia=%s, mota=%s WHERE matuyen=%s""",
                    (tentuyen, diemdi, diemden, thoigian, gia_int, mota, matuyen))
        conn.commit()
        conn.close()
        load_data()
        clear_input()
        entry_matuyen.config(state="normal")
        messagebox.showinfo("Thành công", "Cập nhật thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# ====== Nút chức năng ======
frame_btn = tk.Frame(root)
frame_btn.pack(pady=15)

tk.Button(frame_btn, text="Thêm mới", width=10, bg="green", fg="white", command=them_tuyen).grid(row=0, column=0, padx=8)
tk.Button(frame_btn, text="Lưu sửa", width=10, bg="orange", fg="white", command=luu_sua).grid(row=0, column=1, padx=8)
tk.Button(frame_btn, text="Xóa", width=10, bg="red", fg="white", command=xoa_tuyen).grid(row=0, column=2, padx=8)
tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=8)
tk.Button(frame_btn, text="Thoát", width=10, bg="gray", fg="white", command=root.quit).grid(row=0, column=4, padx=8)

# ====== Sự kiện click đúp vào bảng để sửa ======
tree.bind("<Double-1>", chon_tuyen_de_sua)

# ====== Load dữ liệu khi mở ======
load_data()

root.mainloop()
