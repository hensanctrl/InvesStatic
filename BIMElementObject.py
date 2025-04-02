class BIMElementObject:
    def __init__(self, revit_element_id, bim_element_id, project_code, total_planned_quantity, unit_price, current_completed_quantity, current_completion_percentage, area, volume, custom_quantity_weight):
        self.revit_element_id = revit_element_id  # 字符串型 “Revit构件Id”
        self.bim_element_id = bim_element_id  # 字符串型 “BIM元素ID”
        self.project_code = project_code  # 字符串型 “清单项目编码”
        self.total_planned_quantity = total_planned_quantity  # 浮点型 “清单计划分配总工程量”
        self.unit_price = unit_price  # 浮点型 “综合单价”
        self.current_completed_quantity = current_completed_quantity  # 浮点型 “本期完成工程量”
        self.current_completion_percentage = current_completion_percentage  # 浮点型 “本期完成百分比”
        self.area = area  # 浮点型 “面积”
        self.volume = volume  # 浮点型 “体积”
        self.custom_quantity_weight = custom_quantity_weight  # 整数型 “自定义数量权重”

# 示例用法
if __name__ == "__main__":
    element = BIMElementObject(
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
    print(element.__dict__)
class class1(object):
    """description of class"""


