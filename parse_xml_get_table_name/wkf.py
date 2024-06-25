# 读取excel 遍历每行
# C D E F G 读取这些列 ，然后处理数据添加到H列
# c列转驼峰命名 d列获取字段类型（c=String，n=Integer）
# F列 = Y(前后去空格)， 加注解@NotBlank(message = E列+"不能为空")
# G列 = Y(前后去空格)， 加注解@Schema(description = E列+G列（有双引号的前面加\\）)
# H列 = G列换行+F列换行+private+ 类型 + 驼峰;
import pandas as pd
import re

# 读取Excel文件
excel_file = 'text.xlsx'  # 替换成你的Excel文件路径
sheet_name = 'Sheet1' 
df = pd.read_excel(excel_file)

# excel_file = '凌志接口一览.xlsx'  # 替换成你的Excel文件路径
# sheet_name = 'T80_适当性管理' 
# df = pd.read_excel(excel_file,sheet_name=sheet_name)
# 定义转驼峰函数
def camel_case(string):
    words = re.split(r'[^a-zA-Z0-9]', string)
    return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(words))

# 初始化空列表用于存储处理后的H列数据
h_column_data = []

# 循环遍历每一行并处理
for index, row in df.iterrows():
    # 获取C列（ob_name列）的内容，并进行驼峰命名处理
    ob_name = row[2]  # 这里假设ob_name列的索引位置是1（第二列）
    camel_case_name = camel_case(ob_name)
    
    # 获取D列（ob_age列）的内容，这里假设是字符串类型，需要根据实际数据类型进行处理
    var_type = str(row[3])  # 假设ob_age列的索引位置是3（第四列）
    if var_type.startswith('N'):
        var_type = 'Integer'
    elif var_type.startswith('C'):
        var_type = 'String'
    else:
        var_type = var_type  # 其他情况保持原始数据类型
    # 处理E列（姓名）和F列（传张三）
    # 处理F列（是否必填）和G列（传张三）
    not_blank = row[5].strip()  # 假设是否必填列的索引位置是5（第六列）
    e_scheme = row[4].strip() + " " + row[6].strip()  # 假设传张三列的索引位置是4（第五列）
    e_scheme = re.sub(r'"', r'\\"', e_scheme)  # 处理双引号的情况
    
    # 根据是否必填添加 @NotBlank 注解
    ifNotBlank = not_blank == 'N'
    if ifNotBlank:
        not_blank=row[4].strip()
        not_blank_message = f'@NotBlank(message = {not_blank} 不能为空)\n'
    else:
        not_blank_message = ''

    e_scheme_annotation = f'@Schema(description = {e_scheme})'
    
    # 组装H列内容
    H_column = f"{not_blank_message}{e_scheme_annotation}\nprivate {var_type} {camel_case_name};"
    
    # 将处理后的H列数据添加到列表中
    h_column_data.append(H_column)
    print(h_column_data)
# 将处理后的H列数据赋值给DataFrame的H列
df['H列'] = h_column_data

# 输出处理后的DataFrame，可以选择保存为新的Excel文件
#print(df)

# 如果要保存为新的Excel文件，使用以下命令
#df.to_excel('output1.xlsx', index=False)
output_file = 'output.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
