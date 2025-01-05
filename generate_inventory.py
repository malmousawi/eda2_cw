#!/usr/bin/env python3

import json
import subprocess

def run(command):
    """Run a shell command and return its output."""
    result = subprocess.run(command, capture_output=True, encoding="UTF-8")
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {command}\n{result.stderr}")
    return result.stdout

def generate_inventory():
    """Generate Ansible inventory from Terraform outputs."""
    try:
        # Fetch IPs from Terraform outputs
        host_vm_ips = json.loads(run(["terraform", "output", "--json", "host_vm_ips"]))
        worker_vm_ips = json.loads(run(["terraform", "output", "--json", "worker_vm_ips"]))
        storage_vm_ips = json.loads(run(["terraform", "output", "--json", "storage_vm_ips"]))

        # Access "value" directly (as the data is a list)
        host_vm_ips = host_vm_ips if isinstance(host_vm_ips, list) else host_vm_ips.get("value", [])
        worker_vm_ips = worker_vm_ips if isinstance(worker_vm_ips, list) else worker_vm_ips.get("value", [])
        storage_vm_ips = storage_vm_ips if isinstance(storage_vm_ips, list) else storage_vm_ips.get("value", [])
    except Exception as e:
        print(f"Error generating inventory: {e}")
        return {}

    # Build inventory
    inventory = {
        "_meta": {
            "hostvars": {ip: {"ansible_ssh_host": ip, "ansible_user": "almalinux"} for ip in host_vm_ips + worker_vm_ips + storage_vm_ips}
        },
        "host": {"hosts": host_vm_ips},
        "worker": {"hosts": worker_vm_ips},
        "storage": {"hosts": storage_vm_ips},
    }

    return inventory

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Ansible inventory from Terraform outputs.")
    parser.add_argument("--list", action="store_true", help="Generate full inventory")
    parser.add_argument("--host", help="Generate inventory for a single host")

    args = parser.parse_args()

    if args.list:
        try:
            inventory = generate_inventory()
            print(json.dumps(inventory, indent=4))
        except Exception as e:
            print(f"Error generating inventory: {e}")
            print("{}")
    elif args.host:
        # Single host vars can be returned as an empty object (not used in this setup)
        print(json.dumps({}))
    else:
        parser.print_help()
