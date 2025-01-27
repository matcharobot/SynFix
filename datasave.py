from datasets import load_dataset

swebench = load_dataset('princeton-nlp/SWE-bench', split='test')

# 加载 SWE-bench_Lite 数据集
dataset_lite = load_dataset('princeton-nlp/SWE-bench_Lite', split='test')

# 加载 SWE-bench_Verified 数据集
dataset_verified = load_dataset('princeton-nlp/SWE-bench_Verified', split='test')

# 指定保存路径
full_save_path = 'SWE-bench_Full'
lite_save_path = 'SWE-bench_Lite'
verified_save_path = 'SWE-bench_Verified'

# 保存数据集到指定路径
swebench.save_to_disk(full_save_path)
dataset_lite.save_to_disk(lite_save_path)
dataset_verified.save_to_disk(verified_save_path)

