import os
import redis

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
TARGET_DIRS = {
    "ecoli_queue": "/mnt/storage/decompressed_files/decompressed_ecoli",
    "human_queue": "/mnt/storage/decompressed_files/decompressed_human"
}

def collect_files(directory):
    """Collect all .pdb and .cif files from a directory."""
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return []
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".pdb")
    ]

def queue_files(redis_client, queue_name, files):
    """Queue files into the specified Redis queue."""
    for file in files:
        redis_client.rpush(queue_name, file)
        print(f"Queued file: {file} -> {queue_name}")

def main():
    """Main script logic."""
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    for queue_name, directory in TARGET_DIRS.items():
        print(f"Processing directory: {directory}")
        files = collect_files(directory)
        if files:
            queue_files(redis_client, queue_name, files)
        else:
            print(f"No files found in directory: {directory}")

if __name__ == "__main__":
    main()
