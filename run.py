from sources.paues_aberg import get_links, get_content
from llm import extract_information

import csv
import hashlib
from pathlib import Path


existing_hashes = set()
csv_file = Path("pauesaberg.csv")
if csv_file.exists():
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                existing_hashes.add(row[0])

links = get_links()
new_hashes = set()
new_links = []

for link in links:
    hash = hashlib.sha256(link.encode()).hexdigest()
    new_hashes.add(hash)
    if hash not in existing_hashes:
        new_links.append(link)

# Fetch content for new links
if new_links:
    for link in new_links:
        content = get_content(link)
        if content:
            print(f"Link: {link}")
            print(f"Content: {content}")
            print("-" * 20)

            # Extract information using LLM

            extracted_info = extract_information(content)
            print(f"Political Party: {extracted_info.get('political_party', 'Unknown')}")
            print(f"Political Role: {extracted_info.get('political_role', 'Unknown')}")
            print("-" * 20)

# Save new hashes to CSV
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    for hash in new_hashes:
        writer.writerow([hash])
