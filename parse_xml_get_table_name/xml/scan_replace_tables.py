import os
import re

def load_mapping(mapping_file):
    mapping = {}
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                mapping[parts[0].upper()] = parts[1].lower()
    return mapping

# 匹配表名：可能带 OTC./OTC142. 前缀，也可能没前缀，表名全大写字母数字下划线
# 这里做个宽松匹配，前缀可选
TABLE_NAME_PATTERN = re.compile(r'\b(?:OTC142\.|OTC\.)?([A-Z0-9_]+)\b', re.IGNORECASE)

def replace_table_names_in_sql(sql, mapping, replaced_tables, unknown_tables):
    def replacer(match):
        full_match = match.group(0)     # 整个匹配字符串，比如 OTC142.ETF_CONFIGURATION 或者 ETF_CONFIGURATION
        old_prefix = ''
        old_table = ''
        # 判断是否有前缀
        if full_match.upper().startswith('OTC142.'):
            old_prefix = 'OTC142.'
            old_table = full_match[len('OTC142.'):].upper()
        elif full_match.upper().startswith('OTC.'):
            old_prefix = 'OTC.'
            old_table = full_match[len('OTC.'):].upper()
        else:
            old_prefix = ''
            old_table = full_match.upper()

        # 替换表名
        if old_table in mapping:
            new_table_name = mapping[old_table]
        else:
            new_table_name = old_table.lower()
            unknown_tables.add(old_table)

        # 统一用 lcinfo_source 作为前缀
        replaced_tables.add(new_table_name)
        return f'lcinfo_source.{new_table_name}'

    return TABLE_NAME_PATTERN.sub(replacer, sql)

def process_folder(folder_path, mapping_file):
    mapping = load_mapping(mapping_file)
    replaced_tables = set()
    unknown_tables = set()

    for root, _, files in os.walk(folder_path):
        for fname in files:
            if fname.endswith('.xml'):
                full_path = os.path.join(root, fname)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 用正则替换 XML 中 select, insert, update, delete 标签里的SQL
                new_content = re.sub(
                    r'(<(select|insert|update|delete)[^>]*>)(.*?)(</\2>)',
                    lambda m: m.group(1) + replace_table_names_in_sql(
                        m.group(3), mapping, replaced_tables, unknown_tables
                    ) + m.group(4),
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )

                # 覆盖原文件写入
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'✔ 处理完成并覆盖文件: {fname}')

    print('\n===== 替换后的表名（去重） =====\n')
    for t in sorted(replaced_tables):
        print(t)

    if unknown_tables:
        print('\n===== 未匹配映射，直接小写保留表名 =====\n')
        for t in sorted(unknown_tables):
            print(t)
# 示例路径
if __name__ == "__main__":
    # folder_path = r"D:\your\mybatis\xml\path"     # ← 修改为你的 XML 文件目录
    # mapping_file = r"D:\your\mapping\table_mapping.txt"  # ← 替换为你的映射文件路径
    folder_path = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/xml"     # ← 修改为你的 XML 文件目录
    mapping_file = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/xml/table_mapping.txt"
    
    process_folder(folder_path, mapping_file)
