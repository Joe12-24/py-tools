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
        df = pd.read_excel(xls, sheet_name=sheet_name, usecols=[1, 2])  # 只提取第二列和第三列

        # 初始化空字典用于存储提取的功能号和功能名称的内容
        data_dict = {"功能号": [], "功能名称": []}

        # 循环遍历每一行并处理
        current_func_num = None  # 用于存储当前的功能号
        current_func_name = None  # 用于存储当前的功能名称

        for index, row in df.iterrows():
            # 只处理第二列和第三列
            second_col_value = row.iloc[0].strip() if isinstance(row.iloc[0], str) else ''
            third_col_value = row.iloc[1].strip() if isinstance(row.iloc[1], str) else ''

            # 提取 "功能号" 后面的内容
            if second_col_value == "功能号":
                current_func_num = third_col_value
                print(current_func_num)
            # 提取 "功能名称" 后面的内容
            elif second_col_value == "功能名称":
                current_func_name = third_col_value
            
            # 将提取的功能号和功能名称添加到字典
            if current_func_num :
                data_dict["功能号"].append(current_func_num)
                data_dict["功能名称"].append(current_func_name)
                # 重置，以便提取下一个功能号和功能名称
                current_func_num = None
                current_func_name = None

        # 创建新的 DataFrame 保存提取后的数据
        result_df = pd.DataFrame(data_dict)
        print(data_dict)
        # 将结果写入到新的 Excel 文件
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"提取后的数据已保存到 {output_excel_file} 中。")
