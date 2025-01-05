import os
import redis
import glob
import logging
from subprocess import Popen, PIPE
from multiprocessing import Pool

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
RESULTS_DIR = "/mnt/storage/pipeline_results"
MERIZO_PATH = "/home/almalinux/merizo_search/merizo_search/merizo.py"
PARSER_SCRIPT = "/home/almalinux/results_parser.py"
DATABASE_PATH = "/mnt/storage/cath_foldclassdb/cath-4.3-foldclassdb"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def ensure_directories():
    """Ensure result directories exist for both E. coli and Human."""
    os.makedirs(os.path.join(RESULTS_DIR, "ecoli"), exist_ok=True)
    os.makedirs(os.path.join(RESULTS_DIR, "human"), exist_ok=True)


def fetch_batch_tasks(redis_client, queue_name, batch_size=5):
    """Fetch a batch of tasks from a Redis queue."""
    tasks = redis_client.lrange(queue_name, 0, batch_size - 1)  # Get the first `batch_size` tasks
    if tasks:
        redis_client.ltrim(queue_name, len(tasks), -1)  # Remove the fetched tasks from the queue
    return tasks


def run_merizo(file_path, output_dir):
    """Run Merizo on a file."""
    output_base = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0])
    cmd = [
        "python3", MERIZO_PATH, "easy-search", file_path,
        DATABASE_PATH, output_base, "tmp",
        "--iterate", "--output_headers", "-d", "cpu", "--threads", "1"
    ]
    logging.info(f"Running Merizo on: {file_path}")
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            logging.error(f"Merizo failed for {file_path}:\n{err.decode()}")
        else:
            logging.info(f"Merizo completed successfully for: {file_path}")
    except Exception as e:
        logging.error(f"Exception while running Merizo on {file_path}: {e}")


def is_valid_tsv_file(file_path):
    """Check if a TSV file contains data beyond the header."""
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            if len(lines) > 1:  # Check if there's more than just the header
                return True
    except Exception as e:
        logging.warning(f"Error reading file {file_path}: {e}")
    return False


def run_parser():
    """Run the parser on valid _search.tsv files."""
    tsv_files = glob.glob(os.path.join(RESULTS_DIR, "**/*_search.tsv"), recursive=True)
    for tsv_file in tsv_files:
        if is_valid_tsv_file(tsv_file):  # Only run parser on valid files
            output_dir = os.path.dirname(tsv_file)
            cmd = ["python3", PARSER_SCRIPT, tsv_file, output_dir]
            logging.info(f"Running parser on: {tsv_file}")
            try:
                p = Popen(cmd, stdout=PIPE, stderr=PIPE)
                out, err = p.communicate()
                if p.returncode != 0:
                    logging.error(f"Parser failed for {tsv_file}:\n{err.decode()}")
                else:
                    logging.info(f"Parser completed for: {tsv_file}")
            except Exception as e:
                logging.error(f"Exception while running parser: {e}")
        else:
            logging.warning(f"Skipping invalid or empty file: {tsv_file}")


def process_file(file_info):
    """Process a single file with Merizo."""
    file_path, output_dir = file_info
    run_merizo(file_path, output_dir)


def process_batch(queue_name, results_subdir, batch_size=5):
    """Process a batch of tasks from the Redis queue."""
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    tasks = fetch_batch_tasks(redis_client, queue_name, batch_size=batch_size)

    if not tasks:
        logging.info(f"No tasks found in queue: {queue_name}")
        return

    logging.info(f"Processing {len(tasks)} tasks from queue: {queue_name}")
    pool = Pool(len(tasks))  # Number of processes matches the number of tasks in the batch
    file_infos = [(task, os.path.join(RESULTS_DIR, results_subdir)) for task in tasks]
    pool.map(process_file, file_infos)
    pool.close()
    pool.join()


def process_queue(queue_name, results_subdir, batch_size=5):
    """Process tasks from a Redis queue in batches."""
    while True:
        redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        if redis_client.llen(queue_name) == 0:
            logging.info(f"All tasks completed for queue: {queue_name}")
            break
        process_batch(queue_name, results_subdir, batch_size=batch_size)

    run_parser()


def main():
    """Main pipeline logic."""
    ensure_directories()

    # Process E. coli files in batches
    process_queue("ecoli_queue", "ecoli", batch_size=5)

    # Process Human files in batches
    process_queue("human_queue", "human", batch_size=5)

    logging.info("Pipeline execution completed.")


if __name__ == "__main__":
    main()

