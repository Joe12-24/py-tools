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
                "errorLimit":{
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
                "memstoreThreshold":"90",
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

# 输入的 XML 字符串
xml_input = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xdataTemplates xmlns:ns2="http://www.gtja.com/xdata-templates/">
    <!-- 数据抓取 资管小集合收益率 【全量】 -->
    <ns2:xdata-template fromDs="cpzxn"
    fromTableName="prodn_dm.firk_view" toDs="" toTableName="OTC.gj_firk_view_add"
    systemType="CRM" taskType = "DAYEND" snatchType = "CONDITION" queryCond="TRD_DT > sysdate - 15"
    clearOldDataType="ALL">
        <ns2:column fromName="ID" toName="ID" />
		<ns2:column fromName="SECU_ID" toName="SECU_ID" />
		<ns2:column fromName="SECU_SHT" toName="SECU_SHT" />
		<ns2:column fromName="TRD_CODE" toName="TRD_CODE" />
		<ns2:column fromName="TRD_DT" toName="TRD_DT" />
		<ns2:column fromName="CHG_RAT_1Y" toName="CHG_RAT_1Y" />
		<ns2:column fromName="CHG_RAT_2Y" toName="CHG_RAT_2Y" />
		<ns2:column fromName="CHG_RAT_3Y" toName="CHG_RAT_3Y" />
		<ns2:column fromName="CHG_RAT_5Y" toName="CHG_RAT_5Y" />
		<ns2:column fromName="ENT_TIME" toName="ENT_TIME" />
		<ns2:column fromName="UPD_TIME" toName="UPD_TIME" />
		<ns2:column fromName="GRD_TIME" toName="GRD_TIME" />
		<ns2:column fromName="RS_ID" toName="RS_ID" />
		<ns2:column fromName="REC_ID" toName="REC_ID" />
    </ns2:xdata-template>
</xdataTemplates>
'''

# 转换并打印结果
json_output = xml_to_datax_json(xml_input)
print(json_output)
