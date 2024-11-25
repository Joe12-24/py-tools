import os
import xml.etree.ElementTree as ET
import json

def xml_to_datax_json(xml_string):
    # 解析 XML 字符丄1�7
    root = ET.fromstring(xml_string)

    # 初始匄1�7 JSON 配置模板
    datax_config = {
        "job": {
            "content": [],
            "setting": {
                "speed": {
                    "channel": 32  # 默认并发通道敄1�7
                },
                "errorLimit": {
                    "percentage": 0.1
                }
            }
        }
    }

    # 遍历 xdata-template 节点
    for template in root.findall(".//{http://www.gtja.com/xdata-templates/}xdata-template"):
        from_ds = template.get("fromDs")
        from_table_name = template.get("fromTableName")
        to_table_name = template.get("toTableName")

        # 棢�查必要的属��是否存圄1�7
           # 棢�查必要的属��是否存在，如果缺少则使用默认��1�7
        if not from_ds:
            from_ds = "default_from_ds"  # 使用默认倄1�7
            print(f"警告: 'fromDs' 属��缺失，已使用默认��1�7: {from_ds}")

        if not from_table_name:
            from_table_name = "default_from_table"  # 使用默认倄1�7
            print(f"警告: 'fromTableName' 属��缺失，已使用默认��1�7: {from_table_name}")

        if not to_table_name:
            to_table_name = "default_to_table"  # 使用默认倄1�7
            print(f"警告: 'toTableName' 属��缺失，已使用默认��1�7: {to_table_name}")

        # 初始匄1�7 reader 咄1�7 writer
        reader = {
            "name": "oraclereader",
            "parameter": {
                "username": f"${{{from_ds}_username}}",
                "password": f"${{{from_ds}_password}}",
                "column": [],
                "connection": [
                    {
                        "table": [from_table_name],
                        "jdbcUrl": [f"${{{from_ds}_jdbcUrl}}"]
                    }
                ]
            }
        }

        writer = {
            "name": "oceanbasev10writer",
            "parameter": {
                "username": "${lcinfo_username}",
                "password": "${lcinfo_password}",
                "writeMode": "insert",
                "batchSize": 5000,
                "memstoreThreshold": "90",
                "column": [],
                "connection": [
                    {
                        "table": [to_table_name],
                        "jdbcUrl": "${lcinfo_jdbcUrl}"
                    }
                ]
            }
        }

        # 处理 `clearOldDataType`
        clear_old_data_type = template.get("clearOldDataType")
        if clear_old_data_type == "ALL":
            writer["parameter"]["preSql"] = [f"truncate table {to_table_name}"]
        elif clear_old_data_type == "CONDITION":
            writer["parameter"]["preSql"] = template.get("clearCond")

        # 处理 `queryCond`
        query_cond = template.get("queryCond")
        if query_cond:
            reader["parameter"]["where"] = query_cond

        # 填充列映射1�7
        for column in template.findall(".//{http://www.gtja.com/xdata-templates/}column"):
            writer["parameter"]["column"].append(column.get("toName"))
            reader["parameter"]["column"].append(column.get("fromName"))

        # 射1�7 reader 咄1�7 writer 添加刄1�7 content
        datax_config["job"]["content"].append({
            "reader": reader,
            "writer": writer
        })

    # 转换丄1�7 JSON 格式字符丄1�7
    return json.dumps(datax_config, indent=4, ensure_ascii=False)

def process_single_file(file_path):
    """处理单个 XML 文件"""
    if not os.path.isfile(file_path):
        print(f"指定的文仄1�7 {file_path} 不存在��1�7")
        return

    with open(file_path, "r", encoding="utf-8") as xml_file:
        xml_content = xml_file.read()

    try:
        # 转换 XML 丄1�7 JSON
        json_output = xml_to_datax_json(xml_content)

        # 保存 JSON 文件
        json_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}.json"
        json_path = os.path.join(os.path.dirname(file_path), json_file_name)
        with open(json_path, "w", encoding="utf-8") as json_file:
            json_file.write(json_output)
        print(f"转换完成: {file_path} -> {json_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出锄1�7: {e}")

def process_directory_recursive(directory):
    """递归处理目录及其子目录中的所朄1�7 XML 文件"""
    if not os.path.isdir(directory):
        print(f"指定的目彄1�7 {directory} 不存在或不是文件夹��1�7")
        return

    for root_dir, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".xml"):
                file_path = os.path.join(root_dir, file_name)
                process_single_file(file_path)

def process_files_and_directories(paths):
    """处理文件或目录列衄1�7"""
    for path in paths:
        if os.path.isfile(path):
            process_single_file(path)
        elif os.path.isdir(path):
            process_directory_recursive(path)
        else:
            print(f"路径 {path} 无效，请棢�查��1�7")

# 示例调用
paths_to_process = [
    # "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/xdata/parse_xml_get_table_name/template/xdata/parse_xml_get_table_name/template/xdata/cpzx_asset_conf_alloc.xml",  # 单个文件
    "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/xdata"  # 文件处1�7
]

process_files_and_directories(paths_to_process)
