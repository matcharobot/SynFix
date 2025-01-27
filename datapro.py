import os
import subprocess
import pandas as pd
from datasets import load_dataset
import json

# 加载数据集
dataset = load_dataset("princeton-nlp/SWE-bench_Lite")
data = dataset["test"].to_pandas()

# 提取需要的字段
fields = ["repo", "base_commit", "problem_statement"]
data_to_save = data[fields]

# 创建保存路径
codebase_path = "download/codebase"
os.makedirs(codebase_path, exist_ok=True)

# 用于存储结果的列表
results = []

def clone_and_save(repo_url, commit_hash, save_path):
    """
    克隆代码库并返回是否成功
    """
    if os.path.exists(save_path) and os.listdir(save_path):
        print(f"跳过克隆：目录已存在 -> {save_path}")
        return True
    try:
        # 克隆仓库
        subprocess.run(["git", "clone", repo_url, save_path], check=True)
        # 检出指定提交
        subprocess.run(["git", "checkout", commit_hash], cwd=save_path, check=True)
        print(f"成功克隆并检出：{repo_url} @ {commit_hash}")
        return True
    except Exception as e:
        print(f"失败：{repo_url} @ {commit_hash}, 错误：{e}")
        # 如果失败，清理文件夹
        if os.path.exists(save_path):
            subprocess.run(["rm", "-rf", save_path])
        return False

# 遍历每个实例
for index, row in data_to_save.iterrows():
    repo = row["repo"]
    commit = row["base_commit"]
    problem_statement = row["problem_statement"]
    
    # 构造 Git 仓库的完整 URL
    repo_url = f"https://github.com/{repo}.git"
    repo_name = repo.split('/')[-1]
    
    # 使用 repo 名称和 SHA 值构造唯一路径
    unique_save_path = os.path.join(codebase_path, f"{repo_name}_{commit}")
    
    # 克隆代码库
    if clone_and_save(repo_url, commit, unique_save_path):
        # 如果成功，保存对应的记录
        results.append({
            "repo": repo,
            "base_commit": commit,
            "problem_statement": problem_statement,
            "codebase_path": unique_save_path
        })

# 将结果存储为 JSON 文件
output_path = "download/codebase_with_problem_statements.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=4)
print(f"结果已保存到 {output_path}")
