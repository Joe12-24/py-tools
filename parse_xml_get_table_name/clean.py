import pandas as pd

# 读取Excel文件
excel_file = 'output3.xlsx'  # 替换成你的Excel文件路径
output_file = 'output4.xlsx'  # 替换成输出的Excel文件路径

# 读取Excel文件
df = pd.read_excel(excel_file, engine='openpyxl')

# 去除每个单元格内容的首尾双引号
df = df.applymap(lambda x: x.strip('"') if isinstance(x, str) else x)

# 替换连续出现的两个双引号为一个双引号
df = df.applymap(lambda x: x.replace('""', '"') if isinstance(x, str) else x)

# 保存修改后的Excel文件
df.to_excel(output_file, index=False, engine='openpyxl')
