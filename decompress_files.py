import os
import gzip
import shutil

# Paths
SHARED_DIR = "/mnt/storage"
DECOMPRESSED_DIR = os.path.join(SHARED_DIR, "decompressed_files")
HUMAN_DIR = os.path.join(SHARED_DIR, "alphafold_human")
ECOLI_DIR = os.path.join(SHARED_DIR, "alphafold_ecoli")

DECOMPRESSED_HUMAN_DIR = os.path.join(DECOMPRESSED_DIR, "decompressed_human")
DECOMPRESSED_ECOLI_DIR = os.path.join(DECOMPRESSED_DIR, "decompressed_ecoli")

# Ensure decompressed directories exist
os.makedirs(DECOMPRESSED_HUMAN_DIR, exist_ok=True)
os.makedirs(DECOMPRESSED_ECOLI_DIR, exist_ok=True)

def decompress_gz_file(input_path, output_path):
    """Decompress a single .gz file."""
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Decompressed: {input_path} -> {output_path}")

def decompress_pdb_gz_files_in_directory(source_dir, target_dir):
    """Decompress all .pdb.gz files in a given source directory to a target directory."""
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".pdb.gz"):  # Only process .pdb.gz files
                input_path = os.path.join(root, file)
                output_path = os.path.join(target_dir, os.path.basename(file).replace(".gz", ""))
                if not os.path.exists(output_path):  # Avoid re-decompressing files
                    try:
                        decompress_gz_file(input_path, output_path)
                    except Exception as e:
                        print(f"Error decompressing {input_path}: {e}")

if __name__ == "__main__":
    print("Decompressing human .pdb.gz files...")
    decompress_pdb_gz_files_in_directory(HUMAN_DIR, DECOMPRESSED_HUMAN_DIR)
    print("Decompressing E. coli .pdb.gz files...")
    decompress_pdb_gz_files_in_directory(ECOLI_DIR, DECOMPRESSED_ECOLI_DIR)
    print("Decompression complete.")

