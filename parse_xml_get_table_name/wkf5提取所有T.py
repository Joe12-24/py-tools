import pandas as pd
import re  # 导入正则表达式库

# 读取原始 Excel 文件路径和输出文件路径
input_excel_file = '凌志接口一览.xlsx'  # 替换为你的Excel文件路径
output_excel_file = 'output_T开头_7位数字.xlsx'  # 输出文件路径

# 使用 ExcelFile 加载 Excel 文件
xls = pd.ExcelFile(input_excel_file)
data_dict = {"T开头_7位数字": []}  # 创建一个新的字典来存储匹配的字段

# 创建一个新的 Excel 文件，并设置 engine='openpyxl' 以支持写入
with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
    for sheet_name in xls.sheet_names:
        # 读取每个 sheet 的所有行和列
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # 循环遍历每一行和每一列的单元格
        for index, row in df.iterrows():
            for cell in row:
                # 如果单元格是字符串，去除空格后检查是否符合条件
                cell_value = str(cell).strip() if isinstance(cell, str) else ''
                
                # 使用正则表达式匹配以'T'开头且后面跟随7位数字的字段
                if re.match(r'^T\d{7}$', cell_value):
                    data_dict["T开头_7位数字"].append(cell_value)

        # 创建新的 DataFrame 保存提取后的数据
        result_df = pd.DataFrame(data_dict)

        # 将结果写入到新的 Excel 文件
    result_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"提取后的数据已保存到 {output_excel_file} 中。")
