import tkinter as tk
import subprocess

# 定义待启动程序的类
class Program:
    def __init__(self, name, enabled):
        self.name = name
        self.enabled = enabled

# 创建主窗口
root = tk.Tk()

# 设置窗口标题
root.title("Startup Programs Manager")

# 创建列表框
program_list = tk.Listbox(root, width=20, height=10)
program_list.pack()

# 创建添加按钮
add_button = tk.Button(root, text="Add", command=lambda: add_program())
add_button.pack()

# 创建删除按钮
del_button = tk.Button(root, text="Delete", command=lambda: delete_program())
del_button.pack()

# 创建启动按钮
start_button = tk.Button(root, text="Start", command=lambda: start_programs())
start_button.pack()

# 初始化程序列表
programs = [Program("sleep.py", True),
             Program("Program 2", False),
             Program("Program 3", True)]

# 将初始程序添加到列表框
for program in programs:
    program_list.insert(tk.END, program.name)

# 定义添加程序的函数
def add_program():
    name = input("请输入程序名称：")
    enabled = True if input("启用该程序吗？(y/n) ") == "y" else False
    programs.append(Program(name, enabled))
    program_list.insert(tk.END, name)

# 定义删除程序的函数
def delete_program():
    selection = program_list.curselection()
    if selection:
        program_name = program_list.get(selection[0])
        programs.remove(program_name)
        program_list.delete(selection[0])

# 定义启动程序的函数
def start_programs():
    for program in programs:
        if program.enabled:
            subprocess.Popen(["python", program.name])

# 运行主事件循环
root.mainloop()
