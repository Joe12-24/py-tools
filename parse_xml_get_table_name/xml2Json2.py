import os
import xml.etree.ElementTree as ET
import json

def xml_to_datax_json(xml_string):
    # 解析 XML 字符串
    root = ET.fromstring(xml_string)

    # 初始化 JSON 配置模板
    datax_config = {
        "job": {
            "content": [],
            "setting": {
                "speed": {
                    "channel": 32  # 默认并发通道数
                },
                "errorLimit": {
                    "percentage": 0.1
                }
            }
        }
    }

    # 遍历 xdata-template 节点
    for template in root.findall(".//{http://www.gtja.com/xdata-templates/}xdata-template"):
        # 初始化 reader 和 writer
        reader = {
            "name": "oraclereader",
            "parameter": {
                "username": "${"+template.get("fromDs")+"_username"+"}",
                "password": "${"+template.get("fromDs")+"_password"+"}",
                "column": [],
                "connection": [
                    {
                        "table": [template.get("fromTableName")],
                        "jdbcUrl": ["${"+template.get("fromDs")+"_jdbcUrl"+"}"]
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
                        "table": [template.get("toTableName")],
                        "jdbcUrl": "${lcinfo_jdbcUrl}"
                    }
                ]
            }
        }

        # 处理 `clearOldDataType`
        clear_old_data_type = template.get("clearOldDataType")
        if clear_old_data_type == "ALL":
            writer["parameter"]["preSql"] = [f"truncate table {template.get('toTableName')}"]

        # 处理 `queryCond`
        query_cond = template.get("queryCond")
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

def process_all_xml_files_in_directory(directory="/Users/mac/dev/code/py-tools/parse_xml_get_table_name/template/xdata/cpzx_aaahaa01.xml"):
    for file_name in os.listdir(directory):
        if file_name.endswith(".xml"):
            xml_path = os.path.join(directory, file_name)
            with open(xml_path, "r", encoding="utf-8") as xml_file:
                xml_content = xml_file.read()

            # 转换 XML 为 JSON
            json_output = xml_to_datax_json(xml_content)

            # 保存 JSON 文件
            json_file_name = f"{os.path.splitext(file_name)[0]}.json"
            json_path = os.path.join(directory, json_file_name)
            with open(json_path, "w", encoding="utf-8") as json_file:
                json_file.write(json_output)
            print(f"转换完成: {xml_path} -> {json_path}")

# 调用函数处理当前文件夹下的所有 .xml 文件
process_all_xml_files_in_directory()
