import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import tkinter as tk
from DatabaseOperations import DatabaseOperations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartTools:
    """
    A class to handle chart-related operations.
    """
    def __init__(self):
        # 从数据库中读取数据并插入到Treeview控件中
        current_dir = os.path.dirname(os.path.abspath(__file__))+"创智湾BIM统计"
        self.db_ops = DatabaseOperations("创智湾.db",current_dir)

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("投资统计项目图表显示")
        self.root.geometry("1500x1000")
        # 调整窗口位置，使其居中显示
        window_width = 1500
        window_height = 1000
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # 创建Grid，分为2行3列
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.canvas11 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas11.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas12 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas12.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas13 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas13.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.canvas21 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas21.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas22 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas22.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas23 = tk.Canvas(self.frame, width=300, height=300, bg='white')
        self.canvas23.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # 在self.canvas21控件中创建一个matplotlib图表，用柱状图的方式显示self.db_ops中视图"按申报日期统计投资额度"，X轴为按升序排列的"申报日期"，Y轴为"本期完成工程投资额度"
        self.create_chart21()

    def Show(self):
        """
        Placeholder for method to get chart data.
        """
        self.root.mainloop()

    def create_chart21(self):
        """
        Method to create a chart.
        """
        self.db_ops.connect();
        # 从数据库中获取数据
        data = self.db_ops.get_data("按申报日期统计投资额度")
        dates = [row["申报日期"] for row in data]
        amounts = [row["本期完成工程投资额度"] for row in data]
        self.db_ops.close()

         # 设置字体
        font_path = "C:\\Windows\\Fonts\\simsun.ttc"  # 这里使用了宋体字体路径，请根据实际情况调整
        my_font = fm.FontProperties(fname=font_path)

        # 创建图表
        fig, ax = plt.subplots()
        ax.bar(dates, amounts)
        ax.set_xlabel("申报日期", fontproperties=my_font)
        ax.set_ylabel("本期完成工程投资额度", fontproperties=my_font)
        ax.set_title("按申报日期统计投资额度", fontproperties=my_font)

        # 将图表嵌入到Tkinter的Canvas中
        chart = FigureCanvasTkAgg(fig, self.canvas21)
        chart.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def save_chart(self):
        """
        Placeholder for method to save a chart.
        """
        pass