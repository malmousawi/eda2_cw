#!/usr/bin/env python3

import sys
import csv
import os
from collections import defaultdict
import statistics

def main():
    if len(sys.argv) != 3:
        print("Usage: python results_parser.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        sys.exit(1)

    output_file = os.path.join(output_dir, os.path.basename(input_file).replace("_search.tsv", ".parsed"))

    cath_ids = defaultdict(int)
    plDDT_values = []

    try:
        with open(input_file, "r") as fhIn:
            # Skip the header row
            header = next(fhIn).strip().split('\t')
            if len(header) < 4 or header[3] != 'dom_plddt':
                print(f"Error: Unexpected header format in {input_file}")
                sys.exit(1)

            msreader = csv.reader(fhIn, delimiter='\t')
            for i, row in enumerate(msreader, start=2):  # Start index at 2 for proper row tracking
                try:
                    plDDT_values.append(float(row[3]))
                    meta = row[15]
                    cath_ids[meta] += 1  # Adjusted processing logic
                except (ValueError, IndexError) as e:
                    print(f"Error processing row {i}: {e}")
                    continue

        mean_plDDT = statistics.mean(plDDT_values) if plDDT_values else 0

        # writing the results
        with open(output_file, "w", encoding="utf-8") as fhOut:
            fhOut.write(f"#{os.path.basename(input_file)} Results. mean plddt: {mean_plDDT}\n")
            fhOut.write("cath_id,count\n")
            for cath, count in cath_ids.items():
                fhOut.write(f"{cath},{count}\n")

        print(f"Output written to {output_file}")

    except IOError as e:
        print(f"File error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

