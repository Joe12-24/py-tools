import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

SQL_TAGS = {'select', 'update', 'insert', 'delete'}

def extract_sql_from_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        sql_list = []
        for elem in root.iter():
            if elem.tag.lower() in SQL_TAGS:
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
            # 只保留无前缀表名
            if '.' not in full_match:
                found.add(table_name)
    return found

def extract_nextval_sequences(sql_text):
    # 匹配形如 OTC142.SQ_ETF_CONFIGURATION.NEXTVAL 或 otc.some_seq.NEXTVAL
    # 这里带前缀都打印
    pattern = re.compile(r'\b([a-zA-Z0-9_]+\.[a-zA-Z0-9_\.]+)\.NEXTVAL\b', re.IGNORECASE)
    return set(pattern.findall(sql_text))

def walk_and_collect(folder):
    table_to_files = defaultdict(set)    # 无前缀表名 -> 文件集合
    seq_to_files = defaultdict(set)      # 序列名（含前缀） -> 文件集合

    for root, _, files in os.walk(folder):
        for fname in files:
            if fname.lower().endswith('.xml'):
                full_path = os.path.join(root, fname)
                sqls = extract_sql_from_xml(full_path)
                for sql in sqls:
                    tables = extract_table_names(sql)
                    sequences = extract_nextval_sequences(sql)
                    for table in tables:
                        table_to_files[table].add(fname)
                    for seq in sequences:
                        seq_to_files[seq].add(fname)

    return table_to_files, seq_to_files

if __name__ == '__main__':
    folder_path = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/xml"
    tables, sequences = walk_and_collect(folder_path)

    print("未带前缀的表名及其所在文件:")
    for table, files in sorted(tables.items()):
        print(f"{table} : {', '.join(sorted(files))}")

    print("\n所有序列（含.NEXTVAL）及其所在文件:")
    for seq, files in sorted(sequences.items()):
        print(f"{seq}.NEXTVAL : {', '.join(sorted(files))}")
