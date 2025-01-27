import json
import os
import re

# 设置输入和输出文件路径
input_file = "swebench_extracted_data/swebench_data.json"  # 替换为实际路径
output_file = "swebench_filtered_multiple_py_files.json"  # 保存的文件名

# 定义一个函数，统计 patch 中涉及的 .py 文件数量
def count_py_files(patch):
    """
    统计补丁中涉及的 .py 文件数量。
    """
    if not patch:
        return 0
    # 匹配 diff 中的文件名，例如：diff --git a/file.py b/file.py
    py_files = set(re.findall(r"diff --git a/([^\s]+\.py) b/([^\s]+\.py)", patch))
    return len(py_files)

# 确保输入文件存在
if not os.path.exists(input_file):
    raise FileNotFoundError(f"输入文件 {input_file} 不存在，请确认路径是否正确！")

# 加载 JSON 数据
filtered_data = []
with open(input_file, "r") as f:
    for line in f:
        try:
            record = json.loads(line)  # 逐行读取 NDJSON 数据
            py_file_count = count_py_files(record.get("patch", ""))
            if py_file_count >= 2:  # 筛选涉及 2 个或以上 Python 文件的数据
                filtered_data.append(record)
        except json.JSONDecodeError as e:
            print(f"解析失败的行：{line}")
            continue

# 将筛选后的数据保存为新的 JSON 文件
with open(output_file, "w") as f:
    json.dump(filtered_data, f, indent=4)

print(f"筛选后的数据已保存到 {output_file}")
