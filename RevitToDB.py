from cgitb import text
from statistics import quantiles
import BIMElementObject
import tkinter as tk
from tkinter import ttk

class RevitToDB:

    def __init__(self):        
        self.root = tk.Tk()
        self.root.title("BIM构件清单赋工程量")
        self.root.geometry("1500x600")
        self.root['bg']='white'

        # 调整窗口位置，使其居中显示
        window_width = 600
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # root窗口，增加一个Label控件、两个Entry控件和一个Button控件

        self.label = tk.Label(self.root, text="BIM构件清单赋工程量", font=("Arial", 20), bg='white')
        self.label.pack()

        self.textId_label = tk.Label(self.root, text="构件ID:", bg='white')
        self.textId_label.pack()

        self.textId = tk.Entry(self.root, width=50, bg='white')
        self.textId.pack()
  
        self.textQ_label = tk.Label(self.root, text="工程量:", bg='white')
        self.textQ_label.pack()
        self.textQ = tk.Entry(self.root, width=50, bg='white')
        self.textQ.pack()
   
        self.button = tk.Button(self.root, text="赋工程量", font=("Arial", 15), command=self.distribute_quantity)
        self.button.pack()

        # 增加一组Radio控件，用于选择赋工程量的方式，包括“按面积”、“按体积”和“自定义”
        self.v = tk.IntVar(value=2)  # 默认选中按面积        
        tk.Radiobutton(self.root, text="按面积", variable=self.v, value=1, bg='white').pack()
        tk.Radiobutton(self.root, text="按体积", variable=self.v, value=2, bg='white').pack()    
        tk.Radiobutton(self.root, text="自定义", variable=self.v, value=3, bg='white').pack()
       
        # 使用Treeview控件
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # revit_data 
        self.revit_data=""

        # 定义列
        columns = ("Revit构件Id", "BIM元素ID", "清单项目编码", "清单计划分配总工程量", "综合单价", "本期完成工程量", "本期完成百分比", "面积", "体积", "自定义数量权重")
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # 增加退出按钮
        self.exit_button = tk.Button(self.root, text="退出", font=("Arial", 15), command=self.exit_application)
        self.exit_button.pack(pady=10)

    def exit_application(self):
        self.root.quit()
        self.root.destroy()

    def RevitToFrame(self, revit_data):
        # revit_data 是个BIMElementObject对象列表，将其转换为DataFrame
        # 生成一个Treeview控件，逐行显示revit_data中的数据
        self.revit_data = revit_data
        # 插入数据
        for element in revit_data:
            self.tree.insert("", "end", values=(
                element.revit_element_id,
                element.bim_element_id,
                element.project_code,
                element.total_planned_quantity,
                element.unit_price,
                element.current_completed_quantity,
                element.current_completion_percentage,
                element.area,
                element.volume,
                element.custom_quantity_weight
            ))

        self.root.mainloop()
       

    def distribute_quantity(self):
        # 处理赋工程量的逻辑
        # 获取textId和textQ的值
        textId_value = self.textId.get()
        textQ_value = self.textQ.get()
        # 获取选中的赋工程量方式
        distribute_method = self.v.get()
        if distribute_method == 1:
            area_total = 100
            print("按面积赋工程量")
        elif distribute_method == 2:
            volume_total = 200
            print("按体积赋工程量")
        else:
            quantiles = 3
            print("按按自定义比例")

        # 逐个获取Treeview中的数据
        for i, item in enumerate(self.tree.get_children()):
            valuesnew = list(self.tree.item(item, "values"))  # Convert tuple to list
            valuesnew[2] = textId_value  # Modify the list
            valuesnew[3] = textQ_value  # Modify the list
            self.tree.item(item, values=valuesnew)  # Update the tree item with the modified list
            print(valuesnew)

                # 将Treeview中的数据逐项更新到revit_data
        for i, item in enumerate(self.tree.get_children()):
            values = self.tree.item(item, "values")

            t=BIMElementObject.BIMElementObject(
                revit_element_id=values[0],
                bim_element_id=values[1],
                project_code=values[2],
                total_planned_quantity=values[3],
                unit_price=values[4],
                current_completed_quantity=values[5],
                current_completion_percentage=values[6],
                area=values[7],
                volume=values[8],
                custom_quantity_weight=values[9]
            )

            self.revit_data[i] = t

        #此处由包丹添加数据库BIM_DB追加记录操作

        print("赋工程量按钮被点击")

    def RevitToDB(self, df, db_ops):
        """
        将DataFrame数据插入到数据库中
        :param df: DataFrame格式的数据
        :param db_ops: DatabaseOperations对象
        """
        db_ops.connect()
        for index, row in df.iterrows():
            # 假设DataFrame的列名与数据库表的列名一致
            db_ops.cursor.execute(
                "INSERT INTO 分部分项工程清单与计价表 (Revit构件Id, BIM元素ID, 清单项目编码, 清单计划分配总工程量, 综合单价, 本期完成工程量, 本期完成百分比, 面积, 体积, 自定义数量权重) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['Revit构件Id'], row['BIM元素ID'], row['清单项目编码'], row['清单计划分配总工程量'], row['综合单价'], row['本期完成工程量'], row['本期完成百分比'], row['面积'], row['体积'], row['自定义数量权重'])
            )
        db_ops.conn.commit()
        db_ops.close()

    def Check(self, db_ops):
        """
        检查数据库中的数据是否符合某些条件
        :param db_ops: DatabaseOperations对象
        :return: 布尔值，表示检查结果
        """
        db_ops.connect()
        db_ops.cursor.execute("SELECT COUNT(*) FROM 分部分项工程清单与计价表 WHERE 清单项目编码 IS NULL")
        result = db_ops.cursor.fetchone()
        db_ops.close()
        return result[0] == 0

# 示例用法
if __name__ == "__main__":
    from DatabaseOperations import DatabaseOperations

    # 示例Revit数据
    revit_data = [
        {
            "Revit构件Id": "R12345",
            "BIM元素ID": "BIM67890",
            "清单项目编码": "P001",
            "清单计划分配总工程量": 100.0,
            "综合单价": 50.0,
            "本期完成工程量": 20.0,
            "本期完成百分比": 0.2,
            "面积": 30.0,
            "体积": 40.0,
            "自定义数量权重": 5
        }
    ]

    # 创建RevitToDB对象
    revit_to_db = RevitToDB()

    # 将Revit数据转换为DataFrame
    df = revit_to_db.RevitToFrame(revit_data)
    print(df)

    # 创建DatabaseOperations对象
    db_ops = DatabaseOperations("创智湾.db", "G:\\创智湾BIM统计")

    # 将DataFrame数据插入到数据库中
    revit_to_db.RevitToDB(df, db_ops)

    # 检查数据库中的数据
    check_result = revit_to_db.Check(db_ops)
    print(f"检查结果: {check_result}")
