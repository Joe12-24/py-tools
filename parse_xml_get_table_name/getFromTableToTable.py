

# import os
# import xml.etree.ElementTree as ET
# import pandas as pd

# # 定义要遍历的根文件夹路径
# folder_path = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/'

# # 初始化一个空列表来存储提取的数据
# data = []

# # 递归遍历文件夹及其子文件夹
# def parse_xml_files(directory):
#     for entry in os.scandir(directory):
#         if entry.is_file() and entry.name.endswith('.xml'):  # 如果是XML文件
#             file_path = entry.path
#             try:
#                 tree = ET.parse(file_path)
#                 root = tree.getroot()

#                 # 查找所有的ns2:xdata-template标签
#                 for xdata_template in root.findall('.//{*}xdata-template'):
#                     # 提取所需的属性
#                     from_ds = xdata_template.get('fromDs')
#                     from_table_name = xdata_template.get('fromTableName')
#                     to_ds = xdata_template.get('toDs')
#                     to_table_name = xdata_template.get('toTableName')

#                     # 将提取的数据添加到列表中
#                     data.append([from_ds, from_table_name, to_ds, to_table_name])
#             except ET.ParseError as e:
#                 print(f"解析文件 {file_path} 时出错: {e}")
#         elif entry.is_dir():  # 如果是子文件夹，递归调用
#             parse_xml_files(entry.path)

# # 开始解析
# parse_xml_files(folder_path)

# # 将数据转换为DataFrame
# df = pd.DataFrame(data, columns=['fromDs', 'fromTableName', 'toDs', 'toTableName'])

# # 将DataFrame输出到Excel文件
# output_file = 'output.xlsx'
# df.to_excel(output_file, index=False)

# print(f"数据已成功输出到 {output_file}")



import os
import xml.etree.ElementTree as ET
import pandas as pd

# 定义要遍历的根文件夹路径
folder_path = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/'

# 初始化一个空列表来存储提取的数据
data = []

# 递归遍历文件夹及其子文件夹
def parse_xml_files(directory):
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith('.xml'):  # 如果是XML文件
            file_path = entry.path
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                # 查找所有的ns2:xdata-template标签
                for xdata_template in root.findall('.//{*}xdata-template'):
                    # 提取所需的属性
                    from_ds = xdata_template.get('fromDs')
                    from_table_name = xdata_template.get('fromTableName')
                    to_ds = xdata_template.get('toDs')
                    to_table_name = xdata_template.get('toTableName')

                    # 如果属性值不为空，则添加到数据列表
                    # if from_ds and from_table_name and to_ds and to_table_name:
                    data.append([from_ds, from_table_name, to_ds, to_table_name, entry.name])
            except ET.ParseError as e:
                print(f"解析文件 {file_path} 时出错: {e}")
        elif entry.is_dir():  # 如果是子文件夹，递归调用
            parse_xml_files(entry.path)

# 开始解析
parse_xml_files(folder_path)

# 将数据转换为DataFrame
df = pd.DataFrame(data, columns=['fromDs', 'fromTableName', 'toDs', 'toTableName', 'xmlFileName'])

# 去除空白行（如果有）
df.dropna(inplace=True)

# 根据 fromDs 排序
df.sort_values(by='toTableName', inplace=True)
# 去除表名前缀并统一小写进行比较
df['fromTableName_clean'] = df['fromTableName'].apply(lambda x: x.split('.')[-1].lower())
df['toTableName_clean'] = df['toTableName'].apply(lambda x: x.split('.')[-1].lower())

# 筛选出 fromTableName 和 toTableName 不一样的行
df_filtered = df[df['fromTableName_clean'] != df['toTableName_clean']]

# 将数据输出到Excel文件
output_file = 'output2.xlsx'
df_filtered.to_excel(output_file, index=False)

print(f"数据已成功输出到 {output_file}")