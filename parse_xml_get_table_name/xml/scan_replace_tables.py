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

TABLE_PATTERN = re.compile(r'\b(OTC142\.|OTC\.)([A-Z0-9_]+)\b', re.IGNORECASE)

def replace_table_names_in_sql(sql, mapping, replaced_tables, unknown_tables):
    def replacer(match):
        prefix = match.group(1).upper()  # 保持大写
        old_table = match.group(2).upper()

        full_old = prefix + old_table

        if old_table in mapping:
            new_table = mapping[old_table]
            replaced_tables[full_old] = new_table
            return f'lcinfo_source.{new_table}'
        else:
            # 未匹配，原样返回
            unknown_tables.add(match.group(0))  # 保留原大小写和前缀
            return match.group(0)

    return TABLE_PATTERN.sub(replacer, sql)

def process_folder(folder_path, mapping_file):
    mapping = load_mapping(mapping_file)
    replaced_tables = dict()  # 旧表名带前缀(大写) => 新表名(小写)
    unknown_tables = set()    # 保留原始带前缀大小写

    for root, _, files in os.walk(folder_path):
        for fname in files:
            if fname.endswith('.xml'):
                full_path = os.path.join(root, fname)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = re.sub(
                    r'(<(select|insert|update|delete)[^>]*>)(.*?)(</\2>)',
                    lambda m: m.group(1) + replace_table_names_in_sql(
                        m.group(3), mapping, replaced_tables, unknown_tables
                    ) + m.group(4),
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )

                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'✔ 处理完成并覆盖文件: {fname}')

    print('\n===== 替换后的表名（去重） =====\n')
    for old, new in sorted(replaced_tables.items()):
        print(f'{old}  {new}')

    if unknown_tables:
        print('\n===== 未匹配映射，保留原表名 =====\n')
        for t in sorted(unknown_tables):
            print(t)
# 示例路径
if __name__ == "__main__":
    # folder_path = r"D:\your\mybatis\xml\path"     # ← 修改为你的 XML 文件目录
    # mapping_file = r"D:\your\mapping\table_mapping.txt"  # ← 替换为你的映射文件路径
    folder_path = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/xml"     # ← 修改为你的 XML 文件目录
    mapping_file = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/xml/table_mapping.txt"
    
    process_folder(folder_path, mapping_file)
