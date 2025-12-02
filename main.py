import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry

# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="qltuyen_dulich",           
        password="",           
        database="qltuyen_dulich",
        charset='utf8mb4'
    )

# ====== Căn giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("QUẢN LÝ CÁC TUYẾN DU LỊCH")
center_window(root, 700, 500)
root.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ CÁC TUYẾN DU LỊCH", font=("Arial", 18, "bold"))
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill="x")

# Dòng 1
tk.Label(frame_info, text="Mã tuyến").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_matuyen = tk.Entry(frame_info, width=15)
entry_matuyen.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Tên tuyến").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_tentuyen = tk.Entry(frame_info, width=40)
entry_tentuyen.grid(row=0, column=3, padx=5, pady=5, sticky="w")

# Dòng 2
tk.Label(frame_info, text="Điểm đi").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_diemdi = tk.Entry(frame_info, width=25)
entry_diemdi.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Điểm đến").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_diemden = tk.Entry(frame_info, width=25)
entry_diemden.grid(row=1, column=3, padx=5, pady=5, sticky="w")

# Dòng 3
tk.Label(frame_info, text="Số ngày").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_songay = tk.Entry(frame_info, width=12)
entry_songay.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Giá tiền (VNĐ)").grid(row=2, column=2, padx=5, pady=5, sticky="w")
entry_giatien = tk.Entry(frame_info, width=25)
entry_giatien.grid(row=2, column=3, padx=5, pady=5, sticky="w")


# ====== Bảng danh sách tuyến du lịch ======
lbl_ds = tk.Label(root, text="Danh sách các tuyến du lịch", font=("Arial", 10, "bold"))
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("matuyen", "tentuyen", "diemdi", "diemden", "songay", "giatien")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col.capitalize())
tree.heading("matuyen", text="Mã tuyến")
tree.heading("tentuyen", text="Tên tuyến")
tree.heading("diemdi", text="Điểm đi")
tree.heading("diemden", text="Điểm đến")
tree.heading("songay", text="Số ngày")
tree.heading("giatien", text="Giá tiền")

tree.column("matuyen", width=60, anchor="center")
tree.column("tentuyen", width=150)
tree.column("diemdi", width=100)
tree.column("diemden", width=100)
tree.column("songay", width=60, anchor="center")
tree.column("giatien", width=100, anchor="e")


tree.pack(padx=10, pady=5, fill="both")

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
    
def load_data():
    for i in tree.get_children():
        tree.delete(i)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tuyen_dulich")
        for row in cur.fetchall():
            # Format giá tiền
            row = list(row)
            row[5] = f"{int(row[5]):,}".replace(",",".")
            tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    
def them_tuyen():
    matuyen= entry_matuyen.get()
    tentuyen = entry_tentuyen.get()
    diemdi = entry_diemdi.get()
    diemden = entry_diemden.get()
    songay = entry_songay.get()
    giatien = entry_giatien.get()
    

    if matuyen=="" or tentuyen=="" or diemdi=="" or diemden=="" or not songay.isdigit() or not giatien.isdigit():
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ và đúng định dạng!")
        return
    
    try: 
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO tuyen_dulich 
                       (tentuyen, diemdi, diemden, songay, giatien, mota)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (tentuyen, diemdi, diemden, int(songay), int(giatien)))
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
    values = tree.item(selected[0])["values"]
    clear_input()
    entry_matuyen.config(state="normal")
    # Đưa dữ liệu lên form
    values = tree.item(selected)["values"]
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, values[0])
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
    

def luu_tuyen():
    sselected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn tuyến để lưu sửa!")
        return
    matuyen = entry_matuyen.get()

    tentuyen = entry_tentuyen.get().strip()
    diemdi = entry_diemdi.get().strip()
    diemden = entry_diemden.get().strip()
    songay = entry_songay.get().strip()
    giatien = entry_giatien.get().strip()
    

    if not (matuyen and tentuyen and diemdi and diemden and songay.isdigit() and giatien.replace(".","").isdigit()):
        messagebox.showwarning("Lỗi", "Dữ liệu không hợp lệ!")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""UPDATE tuyen_dulich SET 
                        tentuyen=%s, diemdi=%s, diemden=%s, songay=%s, 
                        giatien=%s, mota=%s WHERE matuyen=%s""",
                    (tentuyen, diemdi, diemden, int(songay), int(giatien.replace(".","")), matuyen))
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
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Thêm", width=10, command=them_tuyen).grid(row=0, column=0, padx=8)
tk.Button(frame_btn, text="Sửa", width=10, command=sua_tuyen).grid(row=0, column=1, padx=8)
tk.Button(frame_btn, text="Lưu", width=10, command=luu_tuyen).grid(row=0, column=2, padx=8)
tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=3, padx=8)
tk.Button(frame_btn, text="Xóa", width=10, command=xoa_tuyen).grid(row=0, column=4, padx=8)
tk.Button(frame_btn, text="Thoát", width=10, command=root.quit).grid(row=0, column=5, padx=8)

# ====== Load dữ liệu khi mở chương trình ======
load_data()

root.mainloop()