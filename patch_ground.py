from datasets import load_dataset
import pandas as pd
import os
import json

# Load the SWE-bench Lite dataset
dataset = load_dataset("princeton-nlp/SWE-bench_Lite")

# Convert the test split to a Pandas DataFrame
data = dataset["test"].to_pandas()

# Extract relevant fields
fields = ["repo", "base_commit", "patch", "test_patch", "problem_statement"]
extracted_data = data[fields]

# Create a directory to save the extracted data
output_dir = "swebench_extracted_data"
os.makedirs(output_dir, exist_ok=True)

# Save the data as a JSON file
output_file = os.path.join(output_dir, "swebench_data.json")
extracted_data.to_json(output_file, orient="records", lines=True)

# Also save as a CSV for convenience
csv_file = os.path.join(output_dir, "swebench_data.csv")
extracted_data.to_csv(csv_file, index=False)

print(f"Data has been extracted and saved to:\nJSON: {output_file}\nCSV: {csv_file}")
