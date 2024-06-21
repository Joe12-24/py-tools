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
# Print the unique lines (optional)
for line in unique_lines:
    print(line)
if __name__ == "__main__":

    print("\nTable names involved in <update> tags (after deduplication):")
    