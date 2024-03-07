import re

# 定义要匹配的模式
pattern = r'delete\s+from\s+([^\s]+)'

# 要匹配的文本
text = "delete from otc.L_USER1"

# 在文本中搜索匹配的模式
match = re.search(pattern, text, re.IGNORECASE)

if match:
    table_name = match.group(1)  # 获取匹配到的表名
    print(table_name)  # 输出: otc.L_USER1
