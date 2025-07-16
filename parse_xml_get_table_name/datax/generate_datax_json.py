import os
import json

# === 参数配置 ===
oracle_username = "oracle_user"
oracle_password = "oracle_pass"
oracle_jdbc = "jdbc:oracle:thin:@//oracle_host:1521/orcl"

ob_username = "ob_user"
ob_password = "ob_pass"
ob_jdbc_prefix = "jdbc:mysql://ob_host:2881/your_db?useUnicode=true&characterEncoding=utf8"

# === 输入文件路径 ===
table_list_file = "tables.txt"

# === 输出目录 ===
output_dir = "datax_jobs"
os.makedirs(output_dir, exist_ok=True)

# === 主体模板 ===
def generate_job_json(table_name):
    return {
        "job": {
            "setting": {
                "speed": {"channel": 2}
            },
            "content": [
                {
                    "reader": {
                        "name": "oraclereader",
                        "parameter": {
                            "username": oracle_username,
                            "password": oracle_password,
                            "connection": [
                                {
                                    "querySql": [f"SELECT * FROM {table_name}"],
                                    "jdbcUrl": [oracle_jdbc]
                                }
                            ]
                        }
                    },
                    "writer": {
                        "name": "mysqlwriter",
                        "parameter": {
                            "username": ob_username,
                            "password": ob_password,
                            "column": [],  # 自动列可留空，DataX 会自动映射
                            "preSql": [f"DELETE FROM {table_name}"],
                            "connection": [
                                {
                                    "table": [table_name],
                                    "jdbcUrl": ob_jdbc_prefix
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }

# === 读取表名并生成文件 ===
with open(table_list_file, "r") as f:
    tables = [line.strip() for line in f if line.strip()]

for table in tables:
    json_content = generate_job_json(table)
    file_path = os.path.join(output_dir, f"oracle_to_ob_{table}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)

print(f"✅ 已生成 {len(tables)} 个 DataX 配置文件，保存在目录：{output_dir}")
