from pydoc import text
import tkinter as tk
import tkinter.ttk as ttk
from DatabaseOperations import DatabaseOperations

class applyWindow:
    """
    A class to handle chart-related operations.
    """
    def __init__(self):
        # 从数据库中读取数据并插入到Treeview控件中
        self.db_ops = DatabaseOperations("创智湾.db", "G:\\创智湾BIM统计")
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("模拟录入工程量")

        self.root.geometry("1500x1000")
        # 调整窗口位置，使其居中显示
        window_width = 1500
        window_height = 1000
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # 增加一个Frame控件，作为主窗口的容器
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH)
        # 创建Grid，分为1行2列
        self.canvas11 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas11.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.canvas21 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas21.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 在canvas11中增加一个标签和一个可编辑的Listbox控件，标签为"申报期"，Listbox控件中显示"202503"、"202504"
        self.label_period = tk.Label(self.canvas11, text="申报期")
        self.label_period.pack(pady=10)
        self.listbox_period = tk.Listbox(self.canvas11, height=2)  # 设置高度为2行
        self.listbox_period.pack(pady=10)
        self.listbox_period.insert(0, "202503")
        self.listbox_period.insert(1, "202504")

        # 在canvas11中增加一个标签和一个可编辑的Entry控件，标签为"申报人"，Entry控件中显示"张三"
        self.label_applicant = tk.Label(self.canvas11, text="申报人")
        self.label_applicant.pack(pady=3)
        self.entry_applicant = tk.Entry(self.canvas11)
        self.entry_applicant.pack(pady=3)
        self.entry_applicant.insert(0, "张三")
        # 在canvas11中增加一个标签和一个可编辑的Entry控件，标签为"申报单位"，Entry控件中显示"创智湾"
        self.label_unit = tk.Label(self.canvas11, text="申报单位")
        self.label_unit.pack(pady=3)
        self.entry_unit = tk.Entry(self.canvas11)
        self.entry_unit.pack(pady=3)
        self.entry_unit.insert(0, "创智湾")
        # 在canvas11中增加一个标签和一个可编辑的Entry控件，标签为"申报人单位"，Entry控件中显示"湖州经开"
        self.label_applicant_unit = tk.Label(self.canvas11, text="申报人单位")
        self.label_applicant_unit.pack(pady=3)
        self.entry_applicant_unit = tk.Entry(self.canvas11)
        self.entry_applicant_unit.pack(pady=3)
        self.entry_applicant_unit.insert(0, "湖州经开")

        # 在canvas11中增加按钮，标签为"暂存为草稿"
        self.button_save_draft = tk.Button(self.canvas11, text="暂存为草稿", command=self.save_data)
        self.button_save_draft.pack(pady=3)

        # 在canvas11中增加按钮，标签为"申报数据AI体检"
        self.button_ai_check = tk.Button(self.canvas11, text="申报数据AI体检", command=self.save_data)
        self.button_ai_check.pack(pady=3)

        # 在canvas11中增加按钮，标签为"本期申报上传"
        self.button_upload = tk.Button(self.canvas11, text="本期申报上传", command=self.save_data)
        self.button_upload.pack(pady=3)

        # 在canvas11 中增加一个groupbox控件，标签为"批量操作". 内部增加一个按钮，按钮标签为"批量申报为100%进度"
        self.groupbox_batch = tk.LabelFrame(self.canvas11, text="批量操作", padx=10, pady=10)
        self.groupbox_batch.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.button_batch_apply = tk.Button(self.groupbox_batch, text="批量申报为100%进度", command=self.batch_apply_100)
        self.button_batch_apply.pack(pady=10)

        # 在canvas21中增加一个entry控件
        self.filter_var = tk.StringVar()
        self.filter_var.trace("w", self.update_treeview_filter)
        self.filter_entry = tk.Entry(self.canvas21, textvariable=self.filter_var,bg="yellow")
        self.filter_entry.insert(0, "请输入过滤条件")
        # 设置过滤条件的默认值为"请输入过滤条件"
        self.filter_entry.bind("<FocusIn>", lambda event: self.filter_entry.delete(0, tk.END) if self.filter_entry.get() == "请输入过滤条件" else None)
        self.filter_entry.bind("<FocusOut>", lambda event: self.filter_entry.insert(0, "请输入过滤条件") if not self.filter_entry.get() else None)


        self.filter_entry.pack(pady=10)

        # 在canvas21中增加一个按钮，标签为"按过滤器显示"
        self.button_filter = tk.Button(self.canvas21, text="按过滤器显示", command=self.update_treeview_filter)
        self.button_filter.pack(pady=5)

        self.tree = ttk.Treeview(self.canvas21, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"), show='headings')
        self.tree.heading("col1", text="BIM元素ID", command=lambda: self.sort_treeview("col1", False))
        self.tree.heading("col2", text="清单项目编码", command=lambda: self.sort_treeview("col2", False))
        self.tree.heading("col3", text="累计完成工程量", command=lambda: self.sort_treeview("col3", False))
        self.tree.heading("col4", text="剩余未完成工程量", command=lambda: self.sort_treeview("col4", False))
        self.tree.heading("col5", text="本期申报工程量", command=lambda: self.sort_treeview("col5", False))
        self.tree.heading("col6", text="本期申报百分比", command=lambda: self.sort_treeview("col6", False))
        self.tree.heading("col7", text="已完成百分比", command=lambda: self.sort_treeview("col7", False))
        self.tree.heading("col8", text="已完成进度条", command=lambda: self.sort_treeview("col8", False))

        self.tree.column("col1", width=100)
        self.tree.column("col2", width=100)
        self.tree.column("col3", width=100)
        self.tree.column("col4", width=100)
        self.tree.column("col5", width=100)
        self.tree.column("col6", width=100)
        self.tree.column("col7", width=100)
        self.tree.column("col8", width=300)

        self.tree.pack(expand=True, fill=tk.BOTH)

        # 从数据库中获取数据并插入到TreeView中
        self.db_ops.connect()
        self.data = self.db_ops.get_data2("按构件及清单聚合进度视图")
        for row in self.data:
            self.tree.insert("", "end", values=(row["BIM元素ID"], row["清单项目编码"], row["累计完成工程量"], row["剩余未完成工程量"], "", "", row["已完成百分比"], ""))
        self.db_ops.close()
        # 设置self.tree的行高为40
        self.tree.configure(height=40)

        #在窗口的最下方增加一个状态栏，状态栏文字为"状态栏"
        self.statusbar = tk.Label(self.root, text="状态栏", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        # 设置状态栏的背景色为灰色
        self.statusbar.config(bg="lightgrey")
        # 设置状态栏的文字颜色为黑色
        self.statusbar.config(fg="black")
        # 设置状态栏的字体为微软雅黑，大小为10
        self.statusbar.config(font=("微软雅黑", 10))
        # 设置状态栏的文字为"状态栏"
        self.statusbar.config(text="状态栏")

        # 绑定双击事件
        self.tree.bind('<Double-1>', self.on_double_click)
        # 绑定鼠标移动事件
        self.tree.bind('<Motion>', self.on_mouse_move)

        # 在Treeview中插入进度条
        self.root.after(100, self.insert_progressbars)  # 延迟调用 insert_progressbars


    def update_treeview_filterByBIMid(self, bimIdlist):
        #传入的bimidlist是一个列表，包含了一系列BIM元素ID
        # 在此处增加判断函数，若bimidlist为空，则不进行过滤
        if not bimIdlist:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
            for row in self.data:
                if row["BIM元素ID"] in bimIdlist:
                    self.tree.insert("", "end", values=(row["BIM元素ID"], row["清单项目编码"], row["累计完成工程量"], row["剩余未完成工程量"], "", "", row["已完成百分比"], ""))


        pass

    def update_treeview_filter(self, *args):
        # 获取self.filter_entry的值并转换为小写
        filter_text = self.filter_entry.get().lower()
        print(f"Filter text: {filter_text}")  # 调试信息

        # 在此处增加判断函数，若filter_text为空，则不进行过滤
        if not filter_text:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.data:
            if filter_text in row["BIM元素ID"].lower() or filter_text in row["清单项目编码"].lower():
                self.tree.insert("", "end", values=(row["BIM元素ID"], row["清单项目编码"], row["累计完成工程量"], row["剩余未完成工程量"], "", "", row["已完成百分比"], ""))

    def on_mouse_move(self, event):
        # 获取鼠标所在行
        item = self.tree.identify_row(event.y)
        if item:
            values = self.tree.item(item, "values")
            if values[0] and values[1]:  # 检查第1列和第2列是否有值
                col1_value = values[0]
                col2_value = values[1]
                self.statusbar.config(text=f"第1列: {col1_value}, 第2列: {col2_value}")

    def batch_apply_100(self):
        #将treeview中处于选中状态的行，第5列的值设置为第4列的值，并将第6列的值设置为1-第7列的值
        selected_items = self.tree.selection()
        for item in selected_items:
            values = self.tree.item(item, "values")          
            
            col7 = float(values[6].replace('%', ''))
            col6 = f"{(1 - col7) * 100:.2f}%"
            
            self.tree.item(item, values=(values[0], values[1], values[2], values[3], values[3], col6,values[6], values[7]))
            # 更新进度条
            progressbar, label = self.create_progressbar(self.tree, col7)
            try:
                bbox = self.tree.bbox(item, column="#8")
                if bbox and len(bbox) == 4:
                    x, y, width, height = bbox
                else:
                    # Handle the case where bbox does not return four values
                    x, y, width, height = 0, 0, 0, 0
            except Exception as e:
                # Handle the exception
                x, y, width, height = 0, 0, 0, 0
                print(f"Error getting bbox: {e}")

            progressbar.place(x=x, y=y, width=width, height=height)
            label.place(x=x + width // 2, y=y + height // 2, anchor='e')
            self.tree.set(item, column="#8", value="")
            self.tree.update_idletasks()
            # 更新Treeview           
        self.tree.update_idletasks()  # Force update to display progress bars

    def on_double_click(self, event):
        # 获取双击的单元格
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if column in ["#5", "#6"]:  # 只允许编辑第5、6列
            self.edit_cell_with_entry(item, column)

    def edit_cell_with_entry(self, item, column):
        x, y, width, height = self.tree.bbox(item, column)
        value = self.tree.set(item, column)
        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def on_focus_out(event):
            self.tree.set(item, column, entry.get())
            entry.destroy()

        entry.bind("<FocusOut>", on_focus_out)

    def create_progressbar(self, parent, value):
        style = ttk.Style()
        style.layout('text.Horizontal.TProgressbar',
                     [('Horizontal.Progressbar.trough',
                       {'children': [('Horizontal.Progressbar.pbar',
                                      {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}),
                      ('Horizontal.Progressbar.label', {'sticky': ''})])
        style.configure('text.Horizontal.TProgressbar', text='{}%'.format(value), anchor='center')

        # 定义不同颜色的样式
        style.configure('red.Horizontal.TProgressbar', troughcolor='red', background='red')       
        progressbar_style='red.Horizontal.TProgressbar'
        if value < 100:
            labelcolor = 'blue'
        elif value == 100:
             labelcolor = 'green'
        elif 100 < value < 110:
             labelcolor = 'yellow'
        else:
             labelcolor = 'red'

        progressbar = ttk.Progressbar(parent, style=progressbar_style, orient='horizontal', mode='determinate')
        progressbar['value'] = value

        # 创建标签显示百分比，并右对齐
        label = tk.Label(parent, text=f"{value}%", bg='white', fg=labelcolor, anchor='e')
        return progressbar, label

    def insert_progressbars(self):
        for child in self.tree.get_children():
            values = self.tree.item(child, "values")
            if values[6]:
                progress_str = values[6].replace('%', '')  # Remove the percentage sign
                progress_value = int(float(progress_str))  # Convert to float first, then to int
            else:
                progress_value = 0
            progressbar, label = self.create_progressbar(self.tree, progress_value)
            try:
                bbox = self.tree.bbox(child, column="#8")
                if bbox and len(bbox) == 4:
                    x, y, width, height = bbox
                else:
                    # Handle the case where bbox does not return four values
                    x, y, width, height = 0, 0, 0, 0
            except Exception as e:
                # Handle the exception
                x, y, width, height = 0, 0, 0, 0
                print(f"Error getting bbox: {e}")
            progressbar.place(x=x, y=y, width=width, height=height)
            label.place(x=x + width // 2, y=y + height // 2, anchor='e')
            self.tree.set(child, column="#8", value="")
            self.tree.update_idletasks()  # Force update to display progress bars

    def sort_treeview(self, col, reverse):
        l = []
        for k in self.tree.get_children(''):
            value = self.tree.set(k, col)
            if col == "col7":  # 如果是第7列，去除‘%’后转换为float
                value = float(value.replace('%', ''))
            l.append((value, k))
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def save_data(self):
        # self.db_ops.connect()
        # for child in self.tree.get_children():
        #     values = self.tree.item(child, "values")
        #     col1 = values[0]
        #     col2 = values[1]
        #     col3 = values[2]
        #     progress = values[3]
        #     input1 = values[4]
        #     input2 = values[5]
        #     query = f"INSERT INTO your_table_name (col1, col2, col3, progress, input1, input2) VALUES ('{col1}', '{col2}', '{col3}', '{progress}', '{input1}', '{input2}')"
        #     self.db_ops.execute_query(query)
        # self.db_ops.close()
        pass

    def Show(self):
        """
        Placeholder for method to get chart data.
        """
        self.root.mainloop()

# 创建并显示窗口
if __name__ == "__main__":
    app = applyWindow()
    app.Show()
