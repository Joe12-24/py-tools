import re

def underscore_to_camel(name: str) -> str:
    """
    将下划线命名（支持全大写/全小写）转为驼峰格式
    例如 OP_CODE -> opCode
    """
    name = name.strip().lower()
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), name)

def convert_multiline_input(lines: list[str]) -> list[str]:
    return [underscore_to_camel(line) for line in lines if line.strip()]

def main():
    print("🟢 驼峰命名转换器已启动。每轮输入字段名（支持多行），回车两次执行转换。Ctrl+C 退出。\n")

    while True:
        input_lines = []
        print("请输入字段名（多行，回车两次执行转换）：")
        
        while True:
            try:
                line = input()
                if line.strip() == "":
                    break
                input_lines.append(line)
            except KeyboardInterrupt:
                print("\n⛔ 程序已退出。")
                return

        if not input_lines:
            print("⚠️ 未输入任何字段，请重新输入。\n")
            continue

        result = convert_multiline_input(input_lines)

        print("\n转换结果：")
        print("=" * 20)
        for raw, camel in zip(input_lines, result):
            print(f"{camel}")
        print("=" * 20 + "\n")

if __name__ == "__main__":
    main()
