import pathlib

def process_text_file(text_file_path):
    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        for line_num, line in enumerate(text_file, start=1):
            table_name = line.strip()
            if not table_name:
                continue
            
            table_lower = table_name.lower()
            found = False
            
            # 遍历所有JSON文件（包含子目录）
            for json_path in pathlib.Path('.').rglob('*.json'):
                # 不区分大小写匹配文件名
                if table_lower in json_path.name.lower():
                    found = True
                    # 构建新文件名：行号_原文件名
                    new_name = f"{line_num}_{json_path.name}"
                    new_path = json_path.parent / new_name
                    
                    try:
                        json_path.rename(new_path)
                        print(f"重命名成功: {json_path.name} -> {new_name}")
                    except Exception as e:
                        print(f"重命名失败 {json_path}: {e}")

            if not found:
                print(f"行号 {line_num}: 未找到表 '{table_name}' 对应的文件")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("请通过命令行参数指定文本文件路径")
        print("示例: python script.py tables.txt")
        sys.exit(1)
    
    process_text_file(sys.argv[1])