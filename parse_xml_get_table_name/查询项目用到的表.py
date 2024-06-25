import os ,re
from xml.etree import ElementTree as ET
# 打开文件

unique_lines = []
    # Open the file using 'with' statement to ensure proper file closure
with open('表名.txt', 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Strip leading and trailing whitespace from the line
            stripped_line = line.strip()
            nique_lines = []
            # Check if the stripped line is not already in the list (to avoid duplicates)
            if stripped_line not in unique_lines:
                # Append the stripped line to the list of unique lines
                unique_lines.append(stripped_line)

    
def collect_table_names(file_path):
    all_table_names = set()
    insert_table_names_set = set()
    all_table_names_set = set()
    update_table_names_set = set()
    delete_table_names_set = set()
    tree = ET.parse(file_path)
    root = tree.getroot()
        
    for element in root.iter():
        for table_name in unique_lines:
            text_to_search = str(element.text)  # Convert to string if not already

            # Define your regex pattern
            pattern = r'(?:[.\s\n\r])' + re.escape(table_name) + r'(?:[\s\n\r])'

            # Compile regex with ignore case flag
            regex = re.compile(pattern, re.IGNORECASE)

            # Search for pattern in text_to_search
            if regex.search(text_to_search):
                print(table_name)  
                all_table_names_set.add(table_name)
                
        
    return insert_table_names_set, update_table_names_set,delete_table_names_set,all_table_names_set

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
    directory = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name/' # Current directory
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
    for table_name in all_table_names:
        print(table_name)
