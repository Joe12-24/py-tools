import os
import re
from xml.etree import ElementTree as ET

# 要处理的SQL标签
SQL_TAGS = {'select', 'update', 'insert', 'delete'}

def extract_sql_from_xml(xml_path):
    """
    从XML中提取包含SQL语句的文本
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        sql_list = []

        for elem in root.iter():
            tag = elem.tag.lower()
            if tag in SQL_TAGS:
                sql_text = ''.join(elem.itertext()).strip()
                if sql_text:
                    sql_list.append(sql_text)
        return sql_list
    except Exception as e:
        print(f"[解析失败] {xml_path}: {e}")
        return []
def extract_table_names(sql_text):
    patterns = [
        r'\bfrom\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\bjoin\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\bupdate\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\bdelete\s+from\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\binsert\s+into\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\bmerge\s+into\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\breplace\s+into\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\btruncate\s+table\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\block\s+table\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\bdesc\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
        r'\bexplain\s+.*?\bfrom\s+((?:[a-zA-Z_][\w]*\.)?([a-zA-Z_][\w]*))',
    ]

    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, sql_text, flags=re.IGNORECASE | re.DOTALL)
        for full_match, table_name in matches:
            # 只保留无前缀的，full_match中如果有点就是带前缀，忽略
            if '.' not in full_match:
                found.add(table_name)
    return found
def extract_nextval_sequences(sql_text):
    """
    找出所有 .NEXTVAL 的序列调用
    """
    return set(re.findall(r'\b([\w\.]+)\.NEXTVAL\b', sql_text, re.IGNORECASE))

def walk_and_process_xml(folder):
    all_table_names = set()
    all_sequences = set()

    for root, _, files in os.walk(folder):
        for fname in files:
            if fname.endswith('.xml'):
                full_path = os.path.join(root, fname)
                sql_blocks = extract_sql_from_xml(full_path)
                for sql in sql_blocks:
                    tables = extract_table_names(sql)
                    seqs = extract_nextval_sequences(sql)
                    all_table_names.update(tables)
                    all_sequences.update(seqs)

    return all_table_names, all_sequences

if __name__ == '__main__':
    folder_path = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/xml"
  # 替换成你的目录
    tables, sequences = walk_and_process_xml(folder_path)

    print("✅ 未带库名前缀的表名:")
    for t in sorted(tables):
        print(t)

    print("\n✅ 所有 .NEXTVAL 序列调用:")
    for s in sorted(sequences):
        print(s)
