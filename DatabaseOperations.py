import sqlite3
import os
import pandas as pd
import BIMElementObject

class DatabaseOperations:
    def __init__(self, db_name, project_folder):
        self.db_name = db_name
        self.project_folder = project_folder
        self.db_path = os.path.join(self.project_folder, self.db_name)
        self.conn = None

    def connect(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"数据库文件 {self.db_path} 不存在")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def get_data(self, view_name):
        query = f"SELECT * FROM {view_name} ORDER BY 申报日期 ASC"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data

    def get_data2(self, view_name):
        query = f"SELECT * FROM {view_name} ORDER BY 单位工程 ASC"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data

    def merge_list(self):
        # 实现合并分部分项清单的逻辑
        print("合并分部分项清单")
        # 示例SQL操作
        # 读取project_folder下的所有xlsx文件,然后打开所有包含“清单与计价表”的所有sheet的数据，并从sheet的第7行开始读取数据，并插入到InvesStatic表中
        #清空数据库表"分部分项工程清单与计价表"中的所有数据，但保留本表
        self.cursor.execute("DELETE FROM 分部分项工程清单与计价表")


        import os
        import re
        files = os.listdir(self.project_folder)
        for file in files:
            if re.match(r".*\.xlsx$", file):
                try:
                    fullName = os.path.join(self.project_folder, file)
                    xls = pd.ExcelFile(fullName)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    continue
                for sheet_name in xls.sheet_names:
                    if re.match(".*清单与计价表", sheet_name):

                        project_name="创智湾"

                        df = pd.read_excel(xls, sheet_name=sheet_name)
                        #读取pd所示文件的第3行，第1列的字符串，并截取符号":"之后的字符串
                        a3=df.iloc[1, 0]
                        special_name = a3.split(":")[-1].strip()               
                        
                        #区分单项工程： 桩基、维护工程  地下室   裙房  1#塔楼  2#塔楼
                        #区分单位工程：土建工程  安装工程
                        #区分分部工程：


                        group_name=""
                        df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=6)
                        for index, row in df.iterrows():
                            # 如果第1,2列数据为空，且第3列数据不为空，则第3列数据赋值给小组名
                            if pd.isna(row[0]) and pd.isna(row[5]) and pd.notna(row[2]):
                                group_name = row[2]
                                continue

                            if pd.notna(row[1]):
                                self.cursor.execute("INSERT INTO 分部分项工程清单与计价表 (项目编码) VALUES (?)", (row[1],))
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 建设项目=? WHERE 项目编码=?", (project_name, row[1]))
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 单位工程=? WHERE 项目编码=?", (special_name, row[1]))
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 项目名称_小组名=? WHERE 项目编码=?", (group_name, row[1]))

                            if pd.notna(row[2]):
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 项目名称=? WHERE 项目编码=?", (row[2], row[1]))
                            if pd.notna(row[3]):
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 项目特征=? WHERE 项目编码=?", (row[3], row[1]))
                            if pd.notna(row[4]):
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 计量单位=? WHERE 项目编码=?", (row[4], row[1]))
                            if pd.notna(row[5]):
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 计划总工程量=? WHERE 项目编码=?", (row[5], row[1]))
                            if pd.notna(row[6]):
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 综合单价=? WHERE 项目编码=?", (row[6], row[1]))
                            if pd.notna(row[7]):
                                self.cursor.execute("UPDATE 分部分项工程清单与计价表 SET 合价=?  WHERE 项目编码=?", (row[7], row[1]))  

                self.conn.commit()

    def check_list(self):
        # 实现检查清单的逻辑
        print("检查清单")
        # 示例SQL操作
        self.cursor.execute("SELECT * FROM InvesStatic WHERE 项目编码 IS NULL")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()

# 示例用法
if __name__ == "__main__":
    db_ops = DatabaseOperations("创智湾.db", "G:\\创智湾BIM统计")
    db_ops.connect()
    db_ops.merge_list()
    db_ops.check_list()
    db_ops.close()
