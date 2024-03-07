import os
from xml.etree import ElementTree as ET

def count_tags(file_path):
    insert_count = 0
    update_count = 0

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for element in root.iter():
            if element.tag.endswith('insert'):
                insert_count += 1
            elif element.tag.endswith('update'):
                update_count += 1
                
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")

    return insert_count, update_count

def traverse_directory(directory):
    insert_total = 0
    update_total = 0

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.xml'):
                file_path = os.path.join(root, file_name)
                insert_count, update_count = count_tags(file_path)
                insert_total += insert_count
                update_total += update_count

    return insert_total, update_total

if __name__ == "__main__":
    # directory = '.'  # Current directory
    directory = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name'
    insert_total, update_total = traverse_directory(directory)
    print(f"Total number of <insert> tags: {insert_total}")
    print(f"Total number of <update> tags: {update_total}")
