from lxml import etree
import os

def extract_table_names_from_xml(file_path):
    insert_table_names = set()
    update_table_names = set()

    try:
        tree = etree.parse(file_path)
        root = tree.getroot()

        # 遍历XML文档中的所有元素
        for element in root.iter():
            if element.tag.endswith('insert'):
                table_name = element.get('table')
                if table_name:
                    insert_table_names.add(table_name)
            elif element.tag.endswith('update'):
                table_name = element.get('table')
                if table_name:
                    update_table_names.add(table_name)

    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")

    return insert_table_names, update_table_names

def traverse_directory(directory):
    insert_table_names_set = set()
    update_table_names_set = set()

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.xml'):
                file_path = os.path.join(root, file_name)
                insert_table_names, update_table_names = extract_table_names_from_xml(file_path)
                insert_table_names_set.update(insert_table_names)
                update_table_names_set.update(update_table_names)

    return insert_table_names_set, update_table_names_set

if __name__ == "__main__":
    directory = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name'  # 当前目录
    insert_table_names, update_table_names = traverse_directory(directory)

    print("Insert表名:")
    for table_name in insert_table_names:
        print(table_name)

    print("\nUpdate表名:")
    for table_name in update_table_names:
        print(table_name)
