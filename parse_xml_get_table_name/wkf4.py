import pandas as pd

# 读取原始 Excel 文件路径和输出文件路径
input_excel_file = 'text.xlsx'  # 替换为你的Excel文件路径
output_excel_file = 'output_功能号_功能名称内容.xlsx'  # 输出文件路径

# 使用 ExcelFile 加载 Excel 文件
xls = pd.ExcelFile(input_excel_file)

# 创建一个新的 Excel 文件，并设置 engine='openpyxl' 以支持写入
with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
    for sheet_name in xls.sheet_names:
        # 读取每个 sheet 的数据，只提取第二列和第三列
        df = pd.read_excel(xls, sheet_name=sheet_name, usecols=[1, 2])  # 提取第二列和第三列

        # 初始化空列表用于存储提取的数据
        extracted_data = []

        # 循环遍历每一行并处理
        for index, row in df.iterrows():
            # 只处理第二列和第三列
            second_col_value = row.iloc[0].strip() if isinstance(row.iloc[0], str) else ''
            third_col_value = row.iloc[1].strip() if isinstance(row.iloc[1], str) else ''

            # 等值匹配 "功能号" 或 "功能名称"
            if second_col_value == "功能号" or second_col_value == "功能名称":
                # 将第二列的名称和第三列的值提取
                extracted_data.append([second_col_value, third_col_value])

        # 创建新的 DataFrame 保存提取后的数据
        result_df = pd.DataFrame(extracted_data, columns=["名称", "内容"])

        # 将结果写入到新的 Excel 文件
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"提取后的数据已保存到 {output_excel_file} 中。")
