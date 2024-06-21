import os  # 导入操作系统模块，用于文件路径操作
import re  # 导入正则表达式模块，用于文本替换

def load_old_table_names(file_path):
    """
    从文件中加载旧表名列表
    """
    old_table_names = []  # 创建一个空列表，用于存储旧表名
    with open(file_path, 'r') as file:  # 打开文件以读取
        for line in file:  # 遍历文件的每一行
            # 移除行尾的换行符，并添加otc前缀
            old_table_names.append( line.strip())  # 添加处理过的旧表名到列表中，同时转换为小写
    return old_table_names  # 返回加载的旧表名列表

def replace_table_names_in_file(file_path, old_table_names):
    """
    替换文件中的表名
    """
    with open(file_path, 'r') as file:  # 打开文件以读取
        content = file.read()  # 读取文件内容

    # 依次替换每个旧表名
    for old_table_name in old_table_names:  # 遍历旧表名列表
        # 使用正则表达式进行替换，忽略大小写
        oldname = old_prefix+old_table_name
        newname = new_prefix+old_table_name
        replaced_content = re.sub(r'\b%s\b' % oldname, newname, content, flags=re.IGNORECASE)  # 使用正则表达式替换旧表名为新表名
        #replaced_content = re.sub(r'\b%s\b' % old_prefix+old_table_name, newname, content, flags=re.IGNORECASE)  # 使用正则表达式替换旧表名为新表名

        content = replaced_content  # 更新文件内容

    with open(file_path, 'w') as file:  # 打开文件以写入
        file.write(replaced_content)  # 将替换后的内容写入文件

def traverse_and_replace(directory, old_table_names):
    """
    遍历目录并替换文件中的表名
    """
    for root, dirs, files in os.walk(directory):  # 遍历指定目录及其子目录
        for file_name in files:  # 遍历目录中的文件
            if file_name.endswith('.xml'):  # 如果文件以.xml结尾
                file_path = os.path.join(root, file_name)  # 构建文件的完整路径
                replace_table_names_in_file(file_path, old_table_names)  # 调用替换函数处理文件

# 指定要遍历的目录和存储旧表名的文件路径
directory_to_search = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name/'  # 要遍历的目录路径
old_table_names_file = '/Users/mac/dev/code/py-tools/parse_xml_get_table_name/表名.txt'  # 包含旧表名的文件路径，每行一个表名
new_prefix = 'OTC142.'  # 要替换成的新表名
old_prefix = 'OTC.'  # 要替换成的新表名
# 加载旧表名列表
old_table_names = load_old_table_names(old_table_names_file)

# 执行遍历和替换
traverse_and_replace(directory_to_search, old_table_names)  # 调用遍历和替换函数，开始处理文件
