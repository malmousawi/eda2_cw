import redis
import subprocess
import os

# Configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = 6379
TASKS = [
    ("ecoli_queue", "/mnt/storage/pipeline_results/ecoli_parsed"),
    ("human_queue", "/mnt/storage/pipeline_results/human_parsed"),
]
PARSER_SCRIPT = "/home/almalinux/results_parser.py"

def process_tasks():
    """
    Fetch and process tasks from Redis queues.
    """
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    for queue, output_dir in TASKS:
        while True:
            task = r.lpop(queue)
            if not task:
                break
            print(f"Processing {task}...")
            subprocess.run(["python3", PARSER_SCRIPT, task, output_dir])

if __name__ == "__main__":
    process_tasks()

