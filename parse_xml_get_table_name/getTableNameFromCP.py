import os
import xml.etree.ElementTree as ET

def process_single_file(file_path):
    """处理单个 XML 文件，仅检查 'prodn_dm' 是否在 fromTableName 中"""
    if not os.path.isfile(file_path):
        print(f"指定的文件 {file_path} 不存在。")
        return

    with open(file_path, "r", encoding="utf-8") as xml_file:
        xml_content = xml_file.read()

    try:
        # 解析 XML 文件
        root = ET.fromstring(xml_content)
        
        # 遍历 xdata-template 节点
        for template in root.findall(".//{http://www.gtja.com/xdata-templates/}xdata-template"):
            from_table_name = template.get("fromTableName", "")
            if "prodn_dm" in from_table_name.lower():
                print(f"发现匹配表名: {from_table_name}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def process_directory_recursive(directory):
    """递归处理目录及其子目录中的所有 XML 文件"""
    if not os.path.isdir(directory):
        print(f"指定的目录 {directory} 不存在或不是文件夹。")
        return

    for root_dir, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".xml"):
                file_path = os.path.join(root_dir, file_name)
                process_single_file(file_path)

def process_files_and_directories(paths):
    """处理文件或目录列表"""
    for path in paths:
        if os.path.isfile(path):
            process_single_file(path)
        elif os.path.isdir(path):
            process_directory_recursive(path)
        else:
            print(f"路径 {path} 无效，请检查。")

# 示例调用
paths_to_process = [
    "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/"  # 文件夹路径
]

process_files_and_directories(paths_to_process)
