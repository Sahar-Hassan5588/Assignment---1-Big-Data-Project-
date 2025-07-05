import os
import json
import csv

# Path to the folder containing JSON files
DATA_DIR = '/Users/saharhassan/InferredBugs/inferredbugs'

# Output CSV file path
OUTPUT_CSV = 'inferredbugs_summary.csv'

# List to store all bugs info
all_bugs = []

# Loop through all files in the folder (and subfolders)
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith('.json'):
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    bug_data = json.load(f)
                    
                    # Extract the fields 
                    bug_info = {
                        'file': bug_data.get('file', ''),
                        'bug_type': bug_data.get('bug_type', ''),
                        'severity': bug_data.get('severity', ''),
                        'line': bug_data.get('line', ''),
                        'qualifier': bug_data.get('qualifier', '').replace('\n', ' ').replace('\r', ''),
                    }
                    all_bugs.append(bug_info)
            except Exception as e:
                print(f"Error reading {full_path}: {e}")

# Write all bug info to CSV
with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['file', 'bug_type', 'severity', 'line', 'qualifier']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for bug in all_bugs:
        writer.writerow(bug)

print(f"Extraction complete! Saved {len(all_bugs)} bugs to {OUTPUT_CSV}")
