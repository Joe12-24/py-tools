import openpyxl
import pandas as pd
import re

# 定义转驼峰函数
def camel_case(string):
    words = re.split(r'[^a-zA-Z0-9]', string.lower())
    return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(words))

# 读取Excel文件和设置输出文件
excel_file = '凌志接口一览.xlsx'  # 替换成你的Excel文件路径
output_file = 'output4.xlsx'

# 使用 ExcelFile 加载 Excel 文件
xls = pd.ExcelFile(excel_file)

# 检查是否至少有一个可见的sheet
visible_sheets = [sheet_name for sheet_name in xls.sheet_names if not xls.book[sheet_name].sheet_state == 'hidden']
if not visible_sheets:
    raise ValueError("Excel文件中没有可见的sheet，请确保至少有一个sheet是可见的或者包含内容的。")

# 创建一个新的 Excel 文件，并设置 engine='openpyxl' 以支持写入
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df = openpyxl.load_workbook('example.xlsx')
    print(df.length)
    for sheet_name in xls.sheet_names:
        # 读取每个 sheet 的数据
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # 初始化空列表用于存储处理后的H列数据
        h_column_data = []

        # 循环遍历每一行并处理
        for index, row in df.iterrows():
            operator_no = row['operator_no']  # 假设operator_no列的名称是'operator_no'

            # 判断是否跳过当前行的条件
            if pd.isna(operator_no) or operator_no.strip() == '' or not re.match(r'^[a-zA-Z_0-9]+$', operator_no):
                h_column_data.append('')
                continue  # 跳过不符合条件的行

            # 判断参数名是否包含中文，包含中文则跳过当前行
            if any('\u4e00' <= char <= '\u9fff' for char in operator_no):
                h_column_data.append('')
                continue  # 跳过包含中文的行

            # 获取字段名并转换为驼峰命名
            ob_name = operator_no
            camel_case_name = camel_case(ob_name)

            # 获取字段类型，这里假设为固定值 String
            var_type = 'String'

            # 获取是否必填列和E、F列的值
            not_blank = row['not_blank']
            e_value = str(row['E']).replace('\n', '').replace('\r', '').strip() if pd.notna(row['E']) else ''
            f_value = str(row['F']).replace('\n', '').replace('\r', '').strip() if pd.notna(row['F']) else ''
            e_scheme = f"{e_value} {f_value}" if e_value and f_value else e_value or f_value
            e_scheme = re.sub(r'"', r'\\"', e_scheme)

            # 根据是否必填添加 @NotBlank 注解
            ifNotBlank = not_blank == 'Y'
            if ifNotBlank:
                not_blank_message = f'@NotBlank(message = "{e_value} 不能为空")\n'
            else:
                not_blank_message = ''

            e_scheme_annotation = f'@Schema(description = "{e_scheme}")'

            # 组装H列内容
            H_column = f"{not_blank_message}{e_scheme_annotation}\nprivate {var_type} {camel_case_name};"

            # 将处理后的H列数据添加到列表中
            h_column_data.append(H_column)

        # 将处理后的H列数据赋值给DataFrame的H列
        df['H列'] = h_column_data

        # 将处理后的数据写入到对应的 sheet 中，并命名 sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"处理后的数据已保存到 {output_file} 中。")
