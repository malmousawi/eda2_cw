#!/usr/bin/env python3

import os
import csv
import json
import statistics
from glob import glob
import logging

# Paths
BASE_DIR = "/mnt/storage/pipeline_results"
PARSED_DIRS = {
    "ecoli": os.path.join(BASE_DIR, "ecoli_parsed"),
    "human": os.path.join(BASE_DIR, "human_parsed")
}
OUTPUT_DIR = BASE_DIR

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_parsed_file(file_path):
    """Process a single .parsed file to extract cath_code counts and mean pLDDT."""
    cath_data = {}
    plddt_values = []
    logging.info(f"Processing file: {file_path}")
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

            # Ensure file has at least the header and one data line
            if len(lines) <= 2:
                logging.warning(f"File has no valid data: {file_path}")
                return {}, None

            # Extract mean pLDDT from the first line
            header = lines[0].strip()
            if "mean plddt" in header:
                try:
                    mean_plddt = float(header.split(":")[-1].strip())
                    plddt_values.append(mean_plddt)
                except ValueError:
                    logging.error(f"Malformed mean pLDDT in {file_path}: {header}")
                    return {}, None

            # Skip the header line
            for line in lines[1:]:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue

                try:
                    # Parse the JSON part and count
                    cath_entry, count = line.rsplit(",", 1)
                    cath_entry = json.loads(cath_entry.strip())
                    cath_code = cath_entry.get("cath", "UNASSIGNED")
                    count = int(count.strip())
                    cath_data[cath_code] = cath_data.get(cath_code, 0) + count
                except (json.JSONDecodeError, ValueError, IndexError) as e:
                    logging.error(f"Malformed line in {file_path}: {line} - Error: {e}")
    except Exception as e:
        logging.error(f"Failed to process file {file_path}: {e}")
    return cath_data, plddt_values

def write_csv(data, output_file, headers):
    """Write data to a CSV file."""
    if not data:
        logging.warning(f"No data to write for: {output_file}")
        return

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)
    logging.info(f"CSV written: {output_file}")

def process_all_parsed_files():
    """Process all .parsed files in both ecoli and human directories."""
    summary_data = []
    plddt_results = {}

    for category, dir_path in PARSED_DIRS.items():
        combined_data = {}
        plddt_values = []
        parsed_files = glob(os.path.join(dir_path, "*.parsed"))
        logging.info(f"Found {len(parsed_files)} .parsed files in {category}.")
        
        for parsed_file in parsed_files:
            file_data, plddt = process_parsed_file(parsed_file)
            for cath_code, count in file_data.items():
                combined_data[cath_code] = combined_data.get(cath_code, 0) + count
            if plddt:
                plddt_values.extend(plddt)
        
        # Write combined CATH summary to CSV
        output_file = os.path.join(OUTPUT_DIR, f"{category}_cath_summary.csv")
        write_csv(
            sorted(combined_data.items(), key=lambda x: x[1], reverse=True),
            output_file,
            headers=["cath_code", "count"]
        )
        
        # Collect pLDDT statistics for this organism
        if plddt_values:
            mean_plddt = round(statistics.mean(plddt_values), 2)
            std_plddt = round(statistics.stdev(plddt_values), 2) if len(plddt_values) > 1 else 0.0
            plddt_results[category] = (mean_plddt, std_plddt)
    
    # Write pLDDT summary to CSV
    plddt_summary = [
        [organism, mean, std]
        for organism, (mean, std) in plddt_results.items()
    ]
    write_csv(plddt_summary, os.path.join(OUTPUT_DIR, "pIDDT_means.csv"), headers=["organism", "mean plddt", "plddt std"])

if __name__ == "__main__":
    process_all_parsed_files()

