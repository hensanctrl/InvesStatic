import tkinter as tk
from tkinter import messagebox, filedialog

# 创建主窗口
root = tk.Tk()
root.title("投资统计项目初始化")
root.geometry("600x400")

# 调整窗口位置，使其居中显示
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# 按钮点击事件处理函数
def set_file_path():
    file_path = filedialog.askopenfilename()
    if file_path:
        progress_text.insert(tk.END, f"设置清单与计价文件路径: {file_path}\n")

def create_db():
    # 这里可以调用之前创建数据库的代码
    progress_text.insert(tk.END, "创建项目统计数据库\n")

def merge_lists():
    progress_text.insert(tk.END, "合并分部分项清单\n")

def read_cost_table():
    progress_text.insert(tk.END, "读取单位工程费用表\n")

def read_bim_schedule():
    progress_text.insert(tk.END, "读取BIM构件ID关联进度表\n")

def show_investment_progress():
    progress_text.insert(tk.END, "逐月显示投资进度\n")

# 创建按钮并设置位置
buttons = [
    ("设置清单与计价文件路径", set_file_path),
    ("创建项目统计数据库", create_db),
    ("合并分部分项清单", merge_lists),
    ("读取单位工程费用表", read_cost_table),
    ("读取BIM构件ID关联进度表", read_bim_schedule),
    ("逐月显示投资进度", show_investment_progress)
]

button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

for button_name, command in buttons:
    button = tk.Button(button_frame, text=button_name, command=command, width=25)
    button.pack(pady=5)

# 创建单行文本框用于设置建筑工程项目名
project_name_label = tk.Label(root, text="建筑工程项目名:")
project_name_label.pack(pady=5, anchor='w', padx=10)
project_name_entry = tk.Entry(root, width=50)
project_name_entry.pack(pady=5, anchor='w', padx=10)

# 创建多行文本框用于显示各项操作进度
progress_text_label = tk.Label(root, text="操作进度:")
progress_text_label.pack(pady=5, anchor='w', padx=10)
progress_text = tk.Text(root, height=10, width=50)
progress_text.pack(pady=5, anchor='w', padx=10)

# 运行主循环
root.mainloop()
