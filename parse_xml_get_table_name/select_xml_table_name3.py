import os ,re
from xml.etree import ElementTree as ET
# 查询当前文件下所有的xml文件，分别统计insert和update中的表名
def collect_table_names(file_path):
    insert_table_names = set()
    update_table_names = set()
    delete_table_names = set()
    all_table_names = set()

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for element in root.iter():
                # 获取标签内的文本内容，跳过注释
            #tag_text = "".join(element.itertext())
            if element.tag.lower() in ['insert', 'update', 'select', 'delete']:
                tag_text = "".join(element.itertext()).strip()
                tag_id = element.get('id')
                if tag_text.lower().startswith('insert'):
                # if element.tag.endswith('insert'):
                    table_name = element.get('table')
                    # tag_text = element.text

                    match = re.search(r'insert\s+into\s+([^\s(]+)', tag_text, re.IGNORECASE| re.DOTALL)
                    if match:
                        table_name = match.group(1)
                    else:
                        print("未找到表名"+tag_id+file_path+tag_text)
                    if table_name:
                        insert_table_names.add(table_name)
                        all_table_names.add(table_name)
                # elif element.tag.endswith('update'):
                elif tag_text.lower().startswith('update'):
                    
                    table_name = element.get('table')
                    # tag_text = element.text

                    # 使用正则表达式匹配表名
                    #match = re.search(r'\bupdate\s+(\w+)\b', tag_text, re.IGNORECASE)
                    #match = re.search(r'\bupdate\s+otc\.(\w+)\b', tag_text, re.IGNORECASE)
                    match = re.search(r'\bUPDATE\b\s+.*?\bSET\b', tag_text, re.IGNORECASE| re.DOTALL)
                    
                    # 正则表达式模式，匹配形如 "otc.TABLE_NAME" 或 "TABLE_NAME" 的表名（包括前缀）
                    #pattern = r'\b(?:\w+\.)?(\w+)\b'
                    #match = re.search(pattern, tag_text)
                    if match:
                        update_content = match.group()
                        match = re.search(r'update\s+([^\s]+)\s+SET', update_content, re.IGNORECASE|re.DOTALL)
                        if match:
                            table_name = match.group(1)
                            
                            # 找到 SET 的位置
                            set_index = match.end()
                            
                            # 在 SET 后面插入 update_time = sysdate
                            updated_tag_text = tag_text[:set_index] + ' LCODER_UPDATE_TIME = sysdate,' + tag_text[set_index:]
                            
                            # 将修改后的内容写回文件
                            with open(file_path, 'r' ,encoding='gbk') as file:
                                data = file.read()
                                updated_data = data.replace(tag_text, updated_tag_text)
                            
                            with open(file_path, 'w',encoding='gbk') as file:
                                file.write(updated_data)
                    else:
                        print("未找到表名"+tag_id+file_path+tag_text)
                    if table_name:
                        update_table_names.add(table_name)
                        all_table_names.add(table_name)
                #elif element.tag.endswith('delete'):
                elif tag_text.lower().startswith('delete'):
                    table_name = element.get('table')
                    # tag_text = element.text
                    pattern = r'delete\s+from\s+([^\s]+)'
                    # pattern = r'delete\s+from\s+([^\s]+)\s+(?:where|<where>)'
                    match = re.search(pattern, tag_text, re.IGNORECASE| re.DOTALL)
                    if match:
                        table_name = match.group(1)
                    else:
                        print("未找到表名"+tag_id+file_path+tag_text)
                    if table_name:
                        delete_table_names.add(table_name)
                        all_table_names.add(table_name)
                    
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")

    return insert_table_names, update_table_names,delete_table_names,all_table_names

def traverse_directory(directory):
    insert_table_names_set = set()
    update_table_names_set = set()
    delete_table_names_set = set()
    all_table_names_set = set()
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.xml'):
                file_path = os.path.join(root, file_name)
                insert_table_names, update_table_names,delete_table_names,all_table_names = collect_table_names(file_path)
                insert_table_names_set.update(insert_table_names)
                update_table_names_set.update(update_table_names)
                delete_table_names_set.update(delete_table_names)
                all_table_names_set.update(all_table_names)

    return insert_table_names_set, update_table_names_set,delete_table_names_set,all_table_names_set

if __name__ == "__main__":
    directory = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name'
    insert_table_names, update_table_names,delete_table_names,all_table_names = traverse_directory(directory)
    print("Number of table names involved in <all> tags:", len(all_table_names))
    print("Number of table names involved in <insert> tags:", len(insert_table_names))
    print("Number of table names involved in <update> tags:", len(update_table_names))
    print("Number of table names involved in <delete> tags:", len(delete_table_names))
    print("Table names involved in <insert> tags:")
    for table_name in insert_table_names:
        print(table_name)
    print("\nTable names involved in <update> tags (after deduplication):")
    for table_name in update_table_names:
        print(table_name)
    print("\nTable names involved in <delete> tags (after deduplication):")
    for table_name in delete_table_names:
        print(table_name)
