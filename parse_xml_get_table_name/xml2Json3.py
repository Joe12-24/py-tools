import os
import xml.etree.ElementTree as ET
import json

def xml_to_datax_json(xml_string,unique_entries):
    # 解析 XML 字符串
    root = ET.fromstring(xml_string)

    # 初始化 JSON 配置模板
    datax_config = {
        "job": {
            "content": [],
            "setting": {
                "speed": {
                    "channel":"#{channel}"  # 默认并发通道数
                },
                "errorLimit": {
                    "percentage": "${percentage}"
                }
            }
        }
    }
    # 用一个集合去重
    
    # 遍历 xdata-template 节点
    for template in root.findall(".//{http://www.gtja.com/xdata-templates/}xdata-template"):
        from_ds = template.get("fromDs")
        from_table_name = template.get("fromTableName")
        to_table_name = template.get("toTableName")
        if from_ds and from_table_name  and 'oracle' not in from_ds and 'ocean' not in from_ds :
            unique_entries.add(from_ds)
        # 检查必要的属性是否存在
         # 检查必要的属性是否存在，如果缺少则使用默认值
        if not from_ds:
            from_ds = "default_from_ds"  # 使用默认值
            print(f"警告: 'fromDs' 属性缺失，已使用默认值: {from_ds}")

        if not from_table_name:
            from_table_name = "default_from_table"  # 使用默认值
            print(f"警告: 'fromTableName' 属性缺失，已使用默认值: {from_table_name}")

        if not to_table_name:
            to_table_name = "default_to_table"  # 使用默认值
            print(f"警告: 'toTableName' 属性缺失，已使用默认值: {to_table_name}")
        
        # 初始化 reader 和 writer
        reader = {
            "name": "${cp_reader}",
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
            "name": "${lc_writer}",
            "parameter": {
                "username": "${lc_username}",
                "password": "${lc_password}",
                "writeMode": "insert",
                "batchSize": "${batchSize}",
                "memstoreThreshold": "${memstoreThreshold}",
                "column": [],
                "connection": [
                    {
                        "table": [to_table_name],
                        "jdbcUrl": "${lc_jdbcUrl}"
                    }
                ]
            }
        }

        # 处理 `clearOldDataType`
        clear_old_data_type = template.get("clearOldDataType")
        clear_cond = template.get("clearCond")
        query_cond = template.get("queryCond")
        # 处理 `clearOldDataType`
        if clear_old_data_type == "ALL":
            writer["parameter"]["preSql"] = [f"truncate table {to_table_name}"]
        elif clear_old_data_type == "CONDITION":
            if clear_cond:  # Ensure clear_cond is not None
                if "truncate" in clear_cond.lower():
                    writer["parameter"]["preSql"] = clear_cond
                else:
                    writer["parameter"]["preSql"] = f"delete table {to_table_name} where {clear_cond}"
            elif clear_cond is None and query_cond is not None:
                writer["parameter"]["preSql"] = f"delete table {to_table_name} where {query_cond}"
                # 处理 `queryCond`
                
                if query_cond:
                    reader["parameter"]["where"] = query_cond

        # 填充列映射
        for column in template.findall(".//{http://www.gtja.com/xdata-templates/}column"):
            writer["parameter"]["column"].append(column.get("toName"))
            reader["parameter"]["column"].append(column.get("fromName"))

        # 将 reader 和 writer 添加到 content
        datax_config["job"]["content"].append({
            "reader": reader,
            "writer": writer
        })


    # 转换为 JSON 格式字符串
    return json.dumps(datax_config, indent=4, ensure_ascii=False)

def process_single_file(file_path,unique_entries):
    """处理单个 XML 文件"""
    if not os.path.isfile(file_path):
        print(f"指定的文件 {file_path} 不存在。")
        return

    with open(file_path, "r", encoding="utf-8") as xml_file:
        xml_content = xml_file.read()

    try:
        # 转换 XML 为 JSON
        json_output = xml_to_datax_json(xml_content,unique_entries)

        # 保存 JSON 文件
        json_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}.json"
        json_path = os.path.join(os.path.dirname(file_path), json_file_name)
        with open(json_path, "w", encoding="utf-8") as json_file:
            json_file.write(json_output)
        print(f"转换完成: {file_path} -> {json_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def process_directory_recursive(directory,unique_entries):
    """递归处理目录及其子目录中的所有 XML 文件"""
    if not os.path.isdir(directory):
        print(f"指定的目录 {directory} 不存在或不是文件夹。")
        return

    for root_dir, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".xml"):
                file_path = os.path.join(root_dir, file_name)
                process_single_file(file_path,unique_entries)

def process_files_and_directories(paths):
    unique_entries = set()
    """处理文件或目录列表"""
    for path in paths:
        if os.path.isfile(path):
            process_single_file(path)
        elif os.path.isdir(path):
            process_directory_recursive(path,unique_entries)
        else:
            print(f"路径 {path} 无效，请检查。")
    # sorted_result = sorted(unique_entries, key=lambda x: x.split(":")[0])
    # sorted_result = sorted(unique_entries, key=lambda x: x.split(":")[0].lower())  # 按 fromDs 排序

    result = list(unique_entries)
    print("\n".join(unique_entries))

# 示例调用
paths_to_process = [
    # "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/xdata/parse_xml_get_table_name/template/xdata/parse_xml_get_table_name/template/xdata/cpzx_asset_conf_alloc.xml",  # 单个文件
    "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/"  # 文件夹
    # "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/fun/gj_g2010_prod_info_base_insert.xml"
]

process_files_and_directories(paths_to_process)
