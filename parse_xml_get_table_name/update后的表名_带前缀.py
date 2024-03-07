import re

def extract_table_name(sql_statement):
    # 正则表达式模式，匹配形如 "otc.TABLE_NAME" 或 "TABLE_NAME" 的表名（包括前缀）
    #pattern = r'\b((?:\w+\.)?\w+)\b'
    #match = re.search(pattern, sql_statement)
    #match = re.search(r'\bupdate\s+(\w+)\b', sql_statement, re.IGNORECASE)
    #match = re.search(r'\bupdate\s+(.*?)\bwhere\b', sql_statement, re.IGNORECASE)
    match = re.search(r'\bUPDATE\b\s+.*?\bSET\b', sql_statement, re.IGNORECASE)
    if match:
        update_content = match.group()
        print(update_content)
        match = re.search(r'update\s+([^\s]+)\s+SET', update_content, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            return table_name
        else:
            return None

    else:
        return None

# 测试示例
sql_statement = "update otc.L_USER SET 1=1"
table_name = extract_table_name(sql_statement)
print(table_name)  # 输出: otc.L_USER
