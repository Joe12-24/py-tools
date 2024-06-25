import pandas as pd
import re
import datetime 
# 定义转驼峰函数
def camel_case(string):
    words = re.split(r'[^a-zA-Z0-9]', string.lower())
    return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(words))

# 读取原始 Excel 文件路径和输出文件路径
input_excel_file = '凌志接口一览.xlsx'  # 替换成你的Excel文件路径
output_excel_file = 'output3.xlsx'

# 使用 ExcelFile 加载 Excel 文件
xls = pd.ExcelFile(input_excel_file)

# 创建一个新的 Excel 文件，并设置 engine='openpyxl' 以支持写入
with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
    for sheet_name in xls.sheet_names:
        # 读取每个 sheet 的数据
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # 初始化空列表用于存储处理后的H列数据
        h_column_data = []

        # 循环遍历每一行并处理
        for index, row in df.iterrows():
            operator_no = row.iloc[2]  # 假设operator_no列的名称是'operator_no'
            if isinstance(operator_no, datetime.datetime):
                h_column_data.append('')
                continue
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
            not_blank = row.iloc[5]  # 假设是否必填列的索引位置是5（第六列）
            e_value = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ''
            f_value = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else ''
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
            H_column = f'{not_blank_message}{e_scheme_annotation}\nprivate {var_type} {camel_case_name};'

            # 将处理后的H列数据添加到列表中
            h_column_data.append(H_column)

        # 将处理后的H列数据赋值给DataFrame的H列
        df['H列'] = h_column_data

        # 将处理后的数据写入到对应的 sheet 中，并命名 sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"处理后的数据已保存到 {output_excel_file} 中。")
