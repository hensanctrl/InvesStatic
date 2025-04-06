from cgitb import text
from gc import enable
from statistics import quantiles
from sklearn.metrics import v_measure_score
from sympy import false
import BIMElementObject
import tkinter as tk
from tkinter import ttk
from DatabaseOperations import DatabaseOperations
import tkinter.messagebox as messagebox
import random


class RevitToDB:

    def __init__(self):        
        self.root = tk.Tk()
        self.root.title("BIM构件清单赋工程量")
        self.root.geometry("4500x2000")
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
  
        self.textQ_label = tk.Label(self.root, text="剩余工程量:", bg='white')
        self.textQ_label.pack()
        self.textQ = tk.Entry(self.root, width=50, bg='white')
        self.textQ.pack()
   
        self.textQ2_label = tk.Label(self.root, text="本次拟分配工程量:", bg='white')
        self.textQ2_label.pack()
        self.textQ2 = tk.Entry(self.root, width=50, bg='white')
        self.textQ2.pack()
   
        self.button = tk.Button(self.root, text="赋工程量", font=("Arial", 15), command=self.distribute_quantity)
        self.button.pack()

        # 增加一组Radio控件，用于选择赋工程量的方式，包括“按面积”、“按体积”和“自定义”
        self.selected = tk.StringVar()  # 默认选中按面积      
        self.selected.set("面积")  # 设置默认值
       
        tk.Radiobutton(self.root, text="按面积", variable=self.selected, value="面积",  selectcolor="yellow", command=self.on_radiobutton_select).pack()
        tk.Radiobutton(self.root, text="按体积", variable=self.selected, value="体积",  selectcolor="yellow", command=self.on_radiobutton_select).pack()    
        tk.Radiobutton(self.root, text="按自定义权重", variable=self.selected, value="权重", selectcolor="yellow", command=self.on_radiobutton_select).pack()

      
  

         # 从数据库中读取数据并插入到Treeview控件中
        db_ops2 = DatabaseOperations("创智湾.db", "G:\\创智湾BIM统计")
        # 新增一个Treeview控件
        self.tree2 = ttk.Treeview(self.root)
        self.tree2.pack(fill=tk.BOTH, expand=True, padx=20)

        # 定义列
        columns2 = ("单位工程", "项目编码", "项目名称", "计量特征", "计量单位", "本项目编码已分配工程量", "计划总工程量","未分配总工程量")
        self.tree2["columns"] = columns2
        for col in columns2:
            self.tree2.heading(col, text=col)
            self.tree2.column(col, width=100)

        # 绑定双击事件
        self.tree2.bind("<Double-1>", self.on_tree2_double_click)
        # 从数据库中读取数据并插入到Treeview控件中
        self.update_tree2_data(db_ops2)
       
        # 使用Treeview控件
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20)

        # revit_data 
        self.revit_data=""

        # 定义列
        columns = ("Revit构件Id", "BIM元素ID", "清单项目编码", "清单计划分配总工程量", "综合单价", "本期完成工程量", "本期完成百分比", "面积", "体积", "自定义数量权重")
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=50)

        #增加添加测试构件伪数据
        self.gen_button = tk.Button(self.root, text="生成伪构件", font=("Arial", 15), command=self.GenerateBIMId)
        self.gen_button.pack(pady=10)

        #增加提交按钮
        self.submit_button = tk.Button(self.root, text="提交", font=("Arial", 15), command=self.Submit)
        self.submit_button.pack(pady=10)



        # 增加退出按钮
        self.exit_button = tk.Button(self.root, text="退出", font=("Arial", 15), command=self.exit_application)
        self.exit_button.pack(pady=10)

        #root的最下方，增加一个状态栏，用于显示操作及运行状态
        self.status_bar = tk.Label(self.root, text="状态栏", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_tree2_data(self, db_ops2):
        # 清空现有数据
        for item in self.tree2.get_children():
            self.tree2.delete(item)

        # 连接数据库并读取视图数据
        db_ops2.connect()
        db_ops2.cursor.execute("SELECT * FROM 按清单编码统计工程量分配情况")
        rows = db_ops2.cursor.fetchall()

        for row in rows:
            self.tree2.insert("", "end", values=row)
        db_ops2.close()

    def get_itemById(self,item,id):
        # 连接数据库并读取视图数据
        db_ops2 = DatabaseOperations("创智湾.db", "G:\\创智湾BIM统计")
        db_ops2.connect()
        #得到第一个匹配的“清单项目编码”
        db_ops2.cursor.execute("SELECT {} FROM 分部分项工程清单与计价表 WHERE 项目编码=?".format(item), (id,))
        row = db_ops2.cursor.fetchone()
        if row:
            db_ops2.close()
            return row[0]
        return None

    def on_radiobutton_select(self):
        distribute_method = self.selected.get()
        if distribute_method == "面积":
            self.status_bar.config(text="选择了按面积分配")
        elif distribute_method == "体积":
            self.status_bar.config(text="选择了按体积分配")
        elif distribute_method == "权重":
            self.status_bar.config(text="选择了按自定义权重分配")
        else:
            self.status_bar.config(text="未选择分配方式")


    def on_tree2_double_click(self, event):
        # 获取被双击的行
        item = self.tree2.selection()[0]
        values = self.tree2.item(item, "values")

        # 提取“清单项目编码”和“未分配总工程量”的值
        project_code = values[1]  # 假设“清单项目编码”在第2列
        remaining_quantity = values[7]  # 假设“未分配总工程量”在第8列

        # 替换self.textId和self.textQ的文字内容
        self.textId.delete(0, tk.END)
        self.textId.insert(0, project_code)
        self.textQ.delete(0, tk.END)
        self.textQ.insert(0, remaining_quantity)

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
        textQ_value = self.textQ2.get()
        if  textQ_value == "":
            messagebox.showwarning("警告", "未输入本次拟分配工程量")
            return
        # 获取选中的赋工程量方式
        distribute_method = self.selected.get()
        if distribute_method not in ["面积", "体积", "权重"]:
            messagebox.showwarning("警告", "未选择分配方式")
            return

        # 逐个获取Treeview中的数据
        area_total = 0
        volume_total = 0
        quantiles_total = 0
        for i, item in enumerate(self.tree.get_children()):
            valuesnew = list(self.tree.item(item, "values"))  # Convert tuple to list

            if distribute_method == "面积":
                # 计算self.revit_data中每个元素的面积和体积的总和
                area_total += float(valuesnew[7])
            elif distribute_method == "体积":
                volume_total += float(valuesnew[8])
            elif distribute_method == "权重":
                quantiles_total += float(valuesnew[9])
        else:
                self.status_bar.config(text="未选择分配方式")
                return

        price = self.get_itemById("综合单价", textId_value)

        # 逐个获取Treeview中的数据
        for i, item in enumerate(self.tree.get_children()):
            valuesnew = list(self.tree.item(item, "values"))  # Convert tuple to list
            valuesnew[2] = textId_value  # Modify the list
            if distribute_method == "面积":
                # 按面积分配
                area = float(valuesnew[7])
                if area_total > 0:
                    valuesnew[3] = float(textQ_value) * (area / area_total)
            elif distribute_method == "体积":
                # 按体积分配
                volume = float(valuesnew[8])
                if volume_total > 0:
                    valuesnew[3] = float(textQ_value) * (volume / volume_total)
            elif distribute_method == "权重":
                # 按自定义权重分配
                custom_quantity_weight = float(valuesnew[9])
                if quantiles_total > 0:
                    if textQ_value == "":
                        textQ_value = 0
                    valuesnew[3] = float(textQ_value) * (custom_quantity_weight / quantiles_total)

            valuesnew[4]=  float(price)  # 计算分配的工程量
            self.tree.item(item, values=valuesnew)  # Update the tree item with the modified list
            print(valuesnew)

                # 将Treeview中的数据逐项更新到revit_data
        self.revit_data = []
        for i, item in enumerate(self.tree.get_children()):
            values = self.tree.item(item, "values")
            t = BIMElementObject.BIMElementObject(
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
            self.revit_data.append(t)

        # 此处由包丹添加数据库BIM_DB追加记录操作
        self.status_bar.config(text="赋值完成")
        print("赋工程量按钮被点击")

    def Submit(self):
        """

        """
        db_ops = DatabaseOperations("创智湾.db", "G:\\创智湾BIM统计")
        db_ops.connect()
        for i, item in enumerate(self.tree.get_children()):
            valuesnew = list(self.tree.item(item, "values"))  # Convert tuple to list

             # 查询BIM_DB中是否存在 Revit构件Id, BIM元素ID, 清单项目编码与valuesnew[0], valuesnew[1], valuesnew[2]均相同的记录
            db_ops.cursor.execute(
                "SELECT COUNT(*) FROM BIM_DB WHERE Revit构件Id=? AND BIM元素ID=? AND 清单项目编码=?",
                (valuesnew[0], valuesnew[1], valuesnew[2])
            )
            result = db_ops.cursor.fetchone()

            if result[0] > 0:
                # 如果存在，则执行更新操作
                db_ops.cursor.execute(
                    "UPDATE BIM_DB SET 本构件计划分配工程量=?, 综合单价=? WHERE Revit构件Id=? AND BIM元素ID=? AND 清单项目编码=?",
                    (valuesnew[3], valuesnew[4], valuesnew[0], valuesnew[1], valuesnew[2])
                )
            else:
                # 如果不存在，则执行插入操作
                db_ops.cursor.execute(
                        "INSERT INTO BIM_DB (Revit构件Id, BIM元素ID, 清单项目编码, 本构件计划分配工程量, 综合单价) VALUES (?, ?, ?, ?, ?)",
                        (valuesnew[0], valuesnew[1], valuesnew[2], valuesnew[3], valuesnew[4])
                )
            #将tree的该行文字颜色变为红色
            self.tree.item(item, tags=("red",))
            self.tree.tag_configure("red", foreground="red")  # 设置标签的颜色为红色

        db_ops.conn.commit()
      #  update_tree2_data(self,db_ops)
        self.update_tree2_data(db_ops)
        db_ops.close()
        self.status_bar.config(text="已追加记录至BIM_DB")

    def GenerateBIMId(self):
        #清空tree1的数据
      

        for item in self.tree.get_children():
            self.tree.delete(item)

        #将self.tree的item默认颜色改为黑色
        self.tree.tag_configure("black", foreground="black")

        # 生成伪构件数据
        revit_data = []
        for i in range(4):  # 生成4个伪构件
            random_id = random.randint(10000000, 99999999)
            id = f"R{random_id}"
            element = BIMElementObject.BIMElementObject(
                revit_element_id=id,
                bim_element_id=id,
                project_code="",
                total_planned_quantity=-1,
                unit_price=-1,
                current_completed_quantity=-1,
                current_completion_percentage=-1,
                # 随机生成面积和体积的值
                area=random.uniform(1, 100),
                volume=random.uniform(1, 100),
                custom_quantity_weight=1
            )
            revit_data.append(element)
            # 将生成的伪构件数据插入到Treeview控件中
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
            "自定义数量权重": 1
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
