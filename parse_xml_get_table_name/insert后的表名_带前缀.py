import re

def extract_table_name(sql_statement):
    # 使用正则表达式匹配表名
    match = re.search(r'insert\s+into\s+([^\s()]+)', sql_statement, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        return table_name
    else:
        return None

# 测试示例
sql_statement = "insert into otc.l_user values"
table_name = extract_table_name(sql_statement)
print(table_name)  # 输出: otc.l_user
