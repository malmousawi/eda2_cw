import os
import redis
import subprocess
import gzip
import shutil

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")  # Default to localhost
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))  # Default port
PIPELINE_SCRIPT = "/home/almalinux/pipeline_script.py"

def decompress_file(file_path):
    """Decompress a .gz file if needed."""
    if file_path.endswith(".gz"):
        decompressed_path = file_path[:-3]  # Remove .gz extension
        print(f"Decompressing: {file_path} -> {decompressed_path}")
        with gzip.open(file_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return decompressed_path
    return file_path

def execute_pipeline(file_name):
    """Execute the pipeline script on the given file."""
    decompressed_file = decompress_file(file_name)
    result = subprocess.run(
        ["python3", PIPELINE_SCRIPT, decompressed_file],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)

def worker_loop():
    """Worker loop to fetch and process tasks from Redis."""
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}")
    print("Fetching tasks from Redis queue: protein_tasks")

    while True:
        file_name = redis_client.lpop("protein_tasks")
        if file_name:
            print(f"Worker processing: {file_name}")
            try:
                execute_pipeline(file_name)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
        else:
            print("No more tasks in the queue. Worker exiting.")
            break

if __name__ == "__main__":
    worker_loop()

