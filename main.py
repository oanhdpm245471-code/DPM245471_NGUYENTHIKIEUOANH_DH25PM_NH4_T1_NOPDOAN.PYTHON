from tkinter import *
root=Tk()
root.title('Quản Lý Tuyến Du Lịch')
root.minsize(height=500, width=600)
Label(root, text='Ứng Dụng Quản Lý Tuyến Du Lịch', fg='red', font=('cambria', 14), width=30).grid(row=0)
Listbox=Listbox(root, width=95, height=20).grid(row=1, columnspan=2)
Label(root, text='Mã Tuyến: ').grid(row=2, column=0)
Entry(root, width=40).grid(row=2, column=1)

Label(root, text='Tên Tuyến: ').grid(row=3, column=0)
Entry(root, width=40).grid(row=3, column=1)

Label(root, text='Địa Điểm Xuất Phát: ').grid(row=4, column=0)
Entry(root, width=40).grid(row=4, column=1)

Button=Frame(root)
Button(Button, text='Thêm').pack(side=LEFT)
Button(Button, text='Xóa').pack(side=LEFT)
Button(Button, text='Sửa').pack(side=LEFT)
Button(Button, text='Hủy').pack(side=LEFT)
Button(Button, text='Lưu').pack(side=LEFT)
Button(Button, text='Thoát', command=root.quit).pack(side=LEFT)
Button.grid(row=5, column=1)
root.mainloop()