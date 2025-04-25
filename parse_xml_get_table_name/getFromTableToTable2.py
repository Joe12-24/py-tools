import os
import xml.etree.ElementTree as ET
import pandas as pd

def get_xml_files(folder_path):
    # 遍历文件夹，获取所有XML文件的路径
    xml_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xml"):
                xml_files.append(os.path.join(root, file))
    return xml_files

def parse_xml(file_path):
    # 解析XML文件，提取需要的数据
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    rows = []
    
    # 找到所有ns2:xdata-template标签
    for template in root.findall(".//ns2:xdata-template", namespaces={"ns2": "http://example.com/ns2"}):
        from_ds = template.get("fromDs")
        from_table_name = template.get("fromTableName")
        to_ds = template.get("toDs")
        to_table_name = template.get("toTableName")
        
        # 去除表名前缀并统一小写，进行比较
        from_table_name = from_table_name.split(".")[-1].lower()
        to_table_name = to_table_name.split(".")[-1].lower()
        
        # 筛选出fromTableName和toTableName不一样的行
        if from_table_name != to_table_name:
            rows.append([from_ds, from_table_name, to_ds, to_table_name, file_path])
    
    return rows

def main(folder_path, output_excel):
    # 获取所有XML文件
    xml_files = get_xml_files(folder_path)
    
    all_rows = []
    
    # 解析每个XML文件，收集数据
    for xml_file in xml_files:
        rows = parse_xml(xml_file)
        all_rows.extend(rows)
    
    # 使用Pandas将数据输出到Excel
    df = pd.DataFrame(all_rows, columns=["fromDs", "fromTableName", "toDs", "toTableName", "XML文件名"])
    
    # 去除空白行
    df.dropna(how="all", inplace=True)
    
    # 按照fromDs排序
    df.sort_values(by="fromDs", inplace=True)
    
    # 输出到Excel
    df.to_excel(output_excel, index=False)

if __name__ == "__main__":
    folder_path = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/"  # 替换为你的文件夹路径
    output_excel = "output3.xlsx"  # 输出的Excel文件名
    main(folder_path, output_excel)
