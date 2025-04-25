def parse_fields(text):
    lines = text.strip().splitlines()
    fields = []
    for line in lines:
        if "\t" not in line:
            continue
        name, comment = line.strip().split("\t", 1)
        camel = to_camel_case(name)
        fields.append({"raw": name, "camel": camel, "comment": comment})
    return fields

def to_camel_case(s):
    parts = s.lower().split("_")
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])

def generate_in_dto(class_name, fields):
    lines = []
    lines.append("@Data")
    lines.append(f"public class {class_name} extends LcInDto implements Serializable {{\n")
    lines.append("    private static final long serialVersionUID = 1L;\n")
    for field in fields:
        lines.append(f"    private String {field['camel']};\n    // {field['comment']}\n")
    lines.append("    /**")
    lines.append("     * 转换为请求参数 Map（大写下划线）")
    lines.append("     */")
    lines.append(f"    public static Map<String, Object> getConvertedParams({class_name} param) {{\n")
    lines.append("        Map<String, Object> map = new HashMap<>();")
    for field in fields:
           lines.append(f"        map.put(\"{field['raw']}\", param.get{upper_first(field['camel'])}());")
    lines.append("        map.put(\"msgId\", param.getMsgId()); // 从基类继承")
    lines.append("        return map;")
    lines.append("    }")
    lines.append("}")
    return "\n".join(lines)

def generate_out_dto(class_name, fields):
    lines = []
    lines.append("@Data")
    lines.append(f"public class {class_name} implements Serializable {{\n")
    lines.append("    private static final long serialVersionUID = 1L;\n")
    for field in fields:
        lines.append(f"    private String {field['camel']}; // {field['comment']}")

        # 空参构造器
    lines.append(f"\n    public {class_name}() {{")
    lines.append("        // 默认构造器")
    lines.append("    }")
    lines.append(f"\n    public {class_name}(JSONObject map) {{")
    for field in fields:
        lines.append(f"        this.{field['camel']} = ParamUtils.getStringParam(map.getString(\"{field['raw']}\"));")
    lines.append("    }")
    lines.append("}")
    return "\n".join(lines)

# 交互式输入
def run():
    print("👉 请输入字段（格式如：CUST_CODE<TAB>客户ID），多行粘贴后回车。输入空行或 exit 退出。\n")
    while True:
        print("\n👂 等待输入字段（Ctrl+C 退出）：")
        lines = []
        while True:
            try:
                line = input()
                if not line.strip():
                    break
                if line.strip().lower() == "exit":
                    return
                lines.append(line)
            except KeyboardInterrupt:
                print("\n⛔ 已退出。")
                return

        input_text = "\n".join(lines)
        fields = parse_fields(input_text)
        if not fields:
            print("⚠️ 输入无效，请重新输入。")
            continue

        in_dto_code = generate_in_dto("GeneratedInDto", fields)
        out_dto_code = generate_out_dto("GeneratedOutDto", fields)

        print("\n====== ✅ InDto 代码 ======\n")
        print(in_dto_code)

        print("\n====== ✅ OutDto 代码 ======\n")
        print(out_dto_code)
def upper_first(s):
    return s[0].upper() + s[1:] if s else s

# 执行入口
if __name__ == "__main__":
    run()
