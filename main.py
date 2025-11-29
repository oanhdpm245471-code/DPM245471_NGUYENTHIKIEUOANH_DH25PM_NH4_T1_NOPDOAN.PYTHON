from tkinter import *
from database import *
def add():
    line=id.get()+'-'+name.get()+'-'+day.get()+'-'+money.get()
    save(line)
    show()
def show():
    dl=read()
    Listbox.delete(0, END)
    for i in dl:
        Listbox.insert(END, i)
root=Tk()
id=StringVar()
name=StringVar()
day=StringVar()
money=StringVar()
root.title('Quản Lý Tuyến Du Lịch')
root.minsize(height=500, width=600)
Label(root, text='Ứng Dụng Quản Lý Tuyến Du Lịch', fg='red', font=('cambria', 14), width=30).grid(row=0)
Listbox=Listbox(root, width=95, height=20)
Listbox.grid(row=1, columnspan=2)
show()
Label(root, text='Mã Tuyến: ').grid(row=2, column=0)
Entry(root, width=40, textvariable=id).grid(row=2, column=1)

Label(root, text='Tên Tuyến: ').grid(row=3, column=0)
Entry(root, width=40, textvariable=name).grid(row=3, column=1)

Label(root, text='Địa Điểm Xuất Phát: ').grid(row=4, column=0)
Entry(root, width=40, textvariable=name).grid(row=4, column=1)

Label(root, text='Địa Điểm Đến: ').grid(row=5, column=0)
Entry(root, width=40, textvariable=name).grid(row=5, column=1)

Label(root, text='Số Ngày Tour: ').grid(row=6, column=0)
Entry(root, width=40, textvariable=day).grid(row=6, column=1)

Label(root, text='Giá Tiền: ').grid(row=7, column=0)
Entry(root, width=40, textvariable=money).grid(row=7, column=1)
button=Frame(root)
Button(button, text='Thêm', command=add).pack(side=LEFT)
Button(button, text='Xóa').pack(side=LEFT)
Button(button, text='Sửa').pack(side=LEFT)
Button(button, text='Hủy').pack(side=LEFT)
Button(button, text='Lưu').pack(side=LEFT)
Button(button, text='Thoát', command=root.quit).pack(side=LEFT)
button.grid(row=8, column=1)

root.mainloop()






