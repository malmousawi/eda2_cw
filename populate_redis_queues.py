import redis
import os

# Configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = 6379
ECOLI_DIR = "/mnt/storage/pipeline_results/ecoli"
HUMAN_DIR = "/mnt/storage/pipeline_results/human"

def has_data(file_path):
    """
    Checks if a file has data past the header line.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        # Check if there's more than one line, where the first line is the header
        return len(lines) > 1

def populate_queue(queue_name, directory):
    """
    Populates a Redis queue with files from a directory that have data past the header line.
    """
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.delete(queue_name)  # Clear existing queue
    files = [
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.endswith("_search.tsv") and has_data(os.path.join(directory, f))
    ]
    for file in sorted(files):
        r.rpush(queue_name, file)
    print(f"Added {len(files)} tasks to {queue_name}.")

def main():
    populate_queue("ecoli_queue", ECOLI_DIR)
    populate_queue("human_queue", HUMAN_DIR)

if __name__ == "__main__":
    main()

