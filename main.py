from tkinter import *
root=Tk()
root.title('Quản Lý Tuyến Du Lịch')
root.minsize(height=500, width=600)
Label(root, text='Ứng Dụng Quản Lý Tuyến Du Lịch', fg='red', font=('cambria', 14), width=30).grid(row=0)
Listbox=Listbox(root, width=80, height=20).grid(row=1, columnspan=2)



root.mainloop()