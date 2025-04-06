import tkinter as tk
import RevitToDB
import BIMElementObject
from tkinter import messagebox, filedialog
from DatabaseOperations import DatabaseOperations
import ChartTools
from DemoApplyWindow import applyWindow
import os

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

# 项目默认设置

file_path = os.path.dirname(os.path.abspath(__file__))+"创智湾BIM统计"
project_name = "创智湾"
db_name = "创智湾.db"

# 创建数据库操作对象
db_ops = DatabaseOperations(db_name, file_path)

# 按钮点击事件处理函数
def set_file_path():
    file_path = filedialog.askopenfilename()
    if file_path:
        progress_text.insert(tk.END, f"设置清单与计价文件路径: {file_path}\n")

def create_db():
    progress_text.insert(tk.END, "创建项目统计数据库\n")
    
    import os
    target_path = file_path + "\\" + db_name
    if os.path.exists(target_path):
        progress_text.insert(tk.END, f"文件 {target_path} 已存在，无法重命名\n")
    else:
        import shutil
        shutil.copy("D:\\SQLite\\invesstatic.db", file_path)
        os.rename(file_path + "\\invesstatic.db", target_path)
    #测试db_ops能否正常打开和关闭数据库
    db_ops.connect()
    db_ops.close()


def merge_lists():
    db_ops.connect()
    db_ops.merge_list()
    db_ops.close()
    progress_text.insert(tk.END, "合并分部分项清单\n")

def read_cost_table():
    progress_text.insert(tk.END, "读取单位工程费用表\n")

def read_bim_schedule():

    #创建一个BIMElementObject类的对象列表
    revit_data = []

    x1=BIMElementObject.BIMElementObject(
        revit_element_id="R12345",
        bim_element_id="BIM67890",
        project_code="P001",
        total_planned_quantity=100.0,
        unit_price=50.0,
        current_completed_quantity=20.0,
        current_completion_percentage=0.2,
        area=30.0,
        volume=40.0,
        custom_quantity_weight=5
        )

    x2=BIMElementObject.BIMElementObject(
        revit_element_id="R12346",
        bim_element_id="BIM67891",
        project_code="P002",
        total_planned_quantity=200.0,
        unit_price=60.0,
        current_completed_quantity=30.0,
        current_completion_percentage=0.3,
        area=40.0,
        volume=50.0,
        custom_quantity_weight=6
        )
    revit_data.append(x1)
    revit_data.append(x2)

    rdb=RevitToDB.RevitToDB()
    rdb.RevitToFrame(revit_data)    
   # revit_data=rdb.revit_data
    # progress_text.insert(tk.END, "读取BIM构件ID关联进度表\n")

def show_investment_progress():
    chartDiagram = ChartTools.ChartTools()
    chartDiagram.Show()


def show_demo_applyfor():
    demoapplyWindow = applyWindow()
    demoapplyWindow.Show()






# 创建按钮并设置位置
buttons = [
    ("设置清单与计价文件路径", set_file_path),
    ("创建项目统计数据库", create_db),
    ("合并分部分项清单", merge_lists),
    ("读取单位工程费用表", read_cost_table),
    ("BIM构件工程量赋值", read_bim_schedule),
    ("逐月显示投资进度", show_investment_progress),
    ("模拟申报", show_demo_applyfor)
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
project_name_entry.insert(0, project_name)

# 创建多行文本框用于显示各项操作进度
progress_text_label = tk.Label(root, text="操作进度:")
progress_text_label.pack(pady=5, anchor='w', padx=10)
progress_text = tk.Text(root, height=10, width=50)
progress_text.pack(pady=5, anchor='w', padx=10)

# 运行主循环
root.mainloop()
