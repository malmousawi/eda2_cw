#!/usr/bin/env python3

import redis
import os
import subprocess
import sys

# Dynamically fetch Redis host and port from environment variables
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
QUEUES = {
    "ecoli_queue": "/mnt/storage/pipeline_results/ecoli_parsed",
    "human_queue": "/mnt/storage/pipeline_results/human_parsed"
}

def run_parser_task(input_file, output_dir):
    """Run the results_parser.py script for the given input file and output directory."""
    try:
        cmd = ["python3", "/home/almalinux/results_parser.py", input_file, output_dir]
        subprocess.run(cmd, check=True)
        print(f"Successfully processed: {input_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing file {input_file}: {e}")
        sys.exit(1)

def process_tasks():
    """Fetch tasks from Redis queues and process them."""
    try:
        client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        for queue, output_dir in QUEUES.items():
            while True:
                task = client.lpop(queue)
                if not task:
                    break
                print(f"Processing task from {queue}: {task}")
                run_parser_task(task, output_dir)
    except redis.ConnectionError as e:
        print(f"Redis connection error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_tasks()

