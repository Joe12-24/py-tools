import os
import re
import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Function
from sqlparse.tokens import DML

# Oracle 函数全集（大小写不敏感，匹配时统一用 upper）
oracle_functions = {
    # 字符串函数
    'SUBSTR', 'INSTR', 'LENGTH', 'REPLACE', 'TRIM', 'LTRIM', 'RTRIM', 'CONCAT', 'UPPER', 'LOWER', 'INITCAP', 'TO_CHAR',
    # 数值函数
    'ABS', 'CEIL', 'FLOOR', 'MOD', 'ROUND', 'TRUNC', 'POWER', 'SQRT', 'EXP', 'LN', 'LOG', 'SIGN',
    # 日期函数
    'SYSDATE', 'SYSTIMESTAMP', 'CURRENT_DATE', 'TO_DATE', 'ADD_MONTHS', 'MONTHS_BETWEEN', 'NEXT_DAY', 'LAST_DAY',
    # 条件函数
    'NVL', 'NVL2', 'NULLIF', 'DECODE', 'CASE',
    # 分析函数
    'ROWNUM', 'ROW_NUMBER', 'RANK', 'DENSE_RANK', 'NTILE', 'LEAD', 'LAG', 'LISTAGG',
    # 聚合函数
    'SUM', 'AVG', 'MAX', 'MIN', 'COUNT', 'STDDEV', 'VARIANCE', 'GROUPING'
}


def read_xml_sqls(folder_path):
    file_sql_map = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xml'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    sqls = extract_sql_from_xml(content)
                    file_sql_map[full_path] = sqls
    return file_sql_map


def extract_sql_from_xml(content):
    # 抽取 <select>, <insert>, <update>, <delete> 中的内容
    pattern = re.compile(r"<(select|insert|update|delete)[^>]*>(.*?)</\1>", re.DOTALL | re.IGNORECASE)
    return [match[1] for match in pattern.findall(content)]



def extract_tables_and_functions(sql, depth=0, max_depth=10):
    if depth > max_depth:
        return set(), set()

    tables = set()
    functions = set()

    statements = sqlparse.parse(sql)
    for stmt in statements:
        for token in stmt.tokens:
            if token.ttype is DML:
                continue
            if isinstance(token, Identifier):
                if token.get_real_name():
                    tables.add(token.get_real_name().upper())
            elif isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    if identifier.get_real_name():
                        tables.add(identifier.get_real_name().upper())
            elif isinstance(token, Function):
                func_name = token.get_name()
                if func_name and func_name.upper() in oracle_functions:
                    functions.add(func_name.upper())
            elif hasattr(token, 'tokens'):
                # 递归调用时传入增加的 depth
                sub_tables, sub_funcs = extract_tables_and_functions(str(token), depth + 1, max_depth)
                tables.update(sub_tables)
                functions.update(sub_funcs)

    # 补充正则函数提取
    regex_funcs = re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(', sql)
    for func in regex_funcs:
        if func.upper() in oracle_functions:
            functions.add(func.upper())

    return tables, functions




def main(folder_path):
    file_sql_map = read_xml_sqls(folder_path)

    for filepath, sql_list in file_sql_map.items():
        all_tables = set()
        all_funcs = set()
        for sql in sql_list:
            tables, funcs = extract_tables_and_functions(sql)
            all_tables.update(tables)
            all_funcs.update(funcs)

        print(f"\n📄 文件: {filepath}")
        print(f"📌 表名: {', '.join(sorted(all_tables)) if all_tables else '无'}")
        print(f"🛠️  用到的函数: {', '.join(sorted(all_funcs)) if all_funcs else '无'}")
        print("-" * 50)


if __name__ == "__main__":
    folder_path = "/Users/mac/dev/code/py-tools/parse_xml_get_table_name/xml"  # 👈 替换为你的路径
    main(folder_path)
