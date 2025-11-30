import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # thay user MySQL của em nếu khác
        password="",           # thay password nếu có
        database="qltuyen_dulich",
        charset='utf8mb4'
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
root.title("QUẢN LÝ CÁC TUYẾN DU LỊCH")
center_window(root, 900, 600)
root.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ CÁC TUYẾN DU LỊCH", font=("Arial", 20, "bold"), fg="darkblue")
lbl_title.pack(pady=15)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root)
frame_info.pack(pady=10, padx=20, fill="x")

# Dòng 1
tk.Label(frame_info, text="Mã tuyến", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
entry_matuyen = tk.Entry(frame_info, width=12, state="readonly", font=("Arial", 10))
entry_matuyen.grid(row=0, column=1, padx=10, pady=8, sticky="w")

tk.Label(frame_info, text="Tên tuyến", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=8, sticky="w")
entry_tentuyen = tk.Entry(frame_info, width=40, font=("Arial", 10))
entry_tentuyen.grid(row=0, column=3, padx=10, pady=8, sticky="w")

# Dòng 2
tk.Label(frame_info, text="Điểm đi", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=8, sticky="w")
entry_diemdi = tk.Entry(frame_info, width=25, font=("Arial", 10))
entry_diemdi.grid(row=1, column=1, padx=10, pady=8, sticky="w")

tk.Label(frame_info, text="Điểm đến", font=("Arial", 10)).grid(row=1, column=2, padx=10, pady=8, sticky="w")
entry_diemden = tk.Entry(frame_info, width=25, font=("Arial", 10))
entry_diemden.grid(row=1, column=3, padx=10, pady=8, sticky="w")

# Dòng 3
tk.Label(frame_info, text="Số ngày", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
entry_songay = tk.Entry(frame_info, width=12, font=("Arial", 10))
entry_songay.grid(row=2, column=1, padx=10, pady=8, sticky="w")

tk.Label(frame_info, text="Giá tiền (VNĐ)", font=("Arial", 10)).grid(row=2, column=2, padx=10, pady=8, sticky="w")
entry_giatien = tk.Entry(frame_info, width=25, font=("Arial", 10))
entry_giatien.grid(row=2, column=3, padx=10, pady=8, sticky="w")

# Dòng 4 - Mô tả
tk.Label(frame_info, text="Mô tả", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=8, sticky="nw")
text_mota = tk.Text(frame_info, width=70, height=4, font=("Arial", 10))
text_mota.grid(row=3, column=1, columnspan=3, padx=10, pady=8, sticky="w")

# ====== Bảng danh sách tuyến du lịch ======
lbl_ds = tk.Label(root, text="Danh sách các tuyến du lịch", font=("Arial", 12, "bold"))
lbl_ds.pack(pady=(20,5), anchor="w", padx=20)

columns = ("matuyen", "tentuyen", "diemdi", "diemden", "songay", "giatien", "mota")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

tree.heading("matuyen", text="Mã tuyến")
tree.heading("tentuyen", text="Tên tuyến")
tree.heading("diemdi", text="Điểm đi")
tree.heading("diemden", text="Điểm đến")
tree.heading("songay", text="Số ngày")
tree.heading("giatien", text="Giá tiền (VNĐ)")
tree.heading("mota", text="Mô tả")

tree.column("matuyen", width=70, anchor="center")
tree.column("tentuyen", width=220)
tree.column("diemdi", width=120)
tree.column("diemden", width=120)
tree.column("songay", width=80, anchor="center")
tree.column("giatien", width=120, anchor="e")
tree.column("mota", width=200)

tree.pack(padx=20, pady=10, fill="both", expand=True)

# ====== Hàm chức năng ======
def clear_input():
    entry_matuyen.config(state="normal")
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.config(state="readonly")
    entry_tentuyen.delete(0, tk.END)
    entry_diemdi.delete(0, tk.END)
    entry_diemden.delete(0, tk.END)
    entry_songay.delete(0, tk.END)
    entry_giatien.delete(0, tk.END)
    text_mota.delete("1.0", tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tuyen_dulich ORDER BY matuyen")
        for row in cur.fetchall():
            # Format giá tiền
            row = list(row)
            row[5] = f"{int(row[5]):,}".replace(",",".")
            tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def them_tuyen():
    tentuyen = entry_tentuyen.get().strip()
    diemdi = entry_diemdi.get().strip()
    diemden = entry_diemden.get().strip()
    songay = entry_songay.get().strip()
    giatien = entry_giatien.get().strip()
    mota = text_mota.get("1.0", tk.END).strip()

    if not (tentuyen and diemdi and diemden and songay.isdigit() and giatien.replace(".","").isdigit()):
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ và đúng định dạng!")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO tuyen_dulich 
                        (tentuyen, diemdi, diemden, songay, giatien, mota) 
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                    (tentuyen, diemdi, diemden, int(songay), int(giatien.replace(".","")), mota))
        conn.commit()
        conn.close()
        load_data()
        clear_input()
        messagebox.showinfo("Thành công", "Thêm tuyến du lịch thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def sua_tuyen():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn tuyến cần sửa!")
        return
    matuyen = tree.item(selected)["values"][0]

    # Đưa dữ liệu lên form
    entry_matuyen.config(state="normal")
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, matuyen)
    entry_matuyen.config(state="readonly")

    values = tree.item(selected)["values"]
    entry_tentuyen.delete(0, tk.END)
    entry_tentuyen.insert(0, values[1])
    entry_diemdi.delete(0, tk.END)
    entry_diemdi.insert(0, values[2])
    entry_diemden.delete(0, tk.END)
    entry_diemden.insert(0, values[3])
    entry_songay.delete(0, tk.END)
    entry_songay.insert(0, values[4])
    entry_giatien.delete(0, tk.END)
    entry_giatien.insert(0, str(values[5]).replace(".", ""))
    text_mota.delete("1.0", tk.END)
    text_mota.insert("1.0", values[6])

def luu_tuyen():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn tuyến để lưu sửa!")
        return
    matuyen = entry_matuyen.get()

    tentuyen = entry_tentuyen.get().strip()
    diemdi = entry_diemdi.get().strip()
    diemden = entry_diemden.get().strip()
    songay = entry_songay.get().strip()
    giatien = entry_giatien.get().strip()
    mota = text_mota.get("1.0", tk.END).strip()

    if not (tentuyen and diemdi and diemden and songay.isdigit() and giatien.replace(".","").isdigit()):
        messagebox.showwarning("Lỗi", "Dữ liệu không hợp lệ!")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""UPDATE tuyen_dulich SET 
                        tentuyen=%s, diemdi=%s, diemden=%s, songay=%s, 
                        giatien=%s, mota=%s WHERE matuyen=%s""",
                    (tentuyen, diemdi, diemden, int(songay), int(giatien.replace(".","")), mota, matuyen))
        conn.commit()
        conn.close()
        load_data()
        clear_input()
        messagebox.showinfo("Thành công", "Cập nhật thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xoa_tuyen():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn tuyến để xóa!")
        return
    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tuyến này?"):
        matuyen = tree.item(selected)["values"][0]
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM tuyen_dulich WHERE matuyen=%s", (matuyen,))
            conn.commit()
            conn.close()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Xóa thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

# ====== Frame nút bấm ======
frame_btn = tk.Frame(root)
frame_btn.pack(pady=15)

tk.Button(frame_btn, text="Thêm mới", width=10, bg="green", fg="white", font=("Arial", 10, "bold"), command=them_tuyen).grid(row=0, column=0, padx=8)
tk.Button(frame_btn, text="Sửa", width=10, bg="orange", fg="white", font=("Arial", 10, "bold"), command=sua_tuyen).grid(row=0, column=1, padx=8)
tk.Button(frame_btn, text="Lưu", width=10, bg="blue", fg="white", font=("Arial", 10, "bold"), command=luu_tuyen).grid(row=0, column=2, padx=8)
tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=8)
tk.Button(frame_btn, text="Xóa", width=10, bg="red", fg="white", font=("Arial", 10, "bold"), command=xoa_tuyen).grid(row=0, column=4, padx=8)
tk.Button(frame_btn, text="Thoát", width=10, bg="gray", fg="white", command=root.quit).grid(row=0, column=5, padx=8)

# ====== Load dữ liệu khi mở chương trình ======
load_data()

root.mainloop()