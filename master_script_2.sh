#!/bin/bash

set -e


sudo chmod 600 /home/almalinux/ds4eng-infra/cnc-environment/ssh_key_1.pem

sleep 3

echo "Step 2: Generate Ansible inventory dynamically"
chmod +x generate_inventory.py
./generate_inventory.py --list > inventory.json

sleep 5

echo "Step 2.5: Update known hosts and share lecturer public key"
ansible-playbook -i generate_inventory.py add_keys.yml

echo "Step 3: Install necessary packages on all VMs"
ansible-playbook -i generate_inventory.py install_packages.yml

sleep 5

echo "Step 4: HTTPD setup"
ansible-playbook -i generate_inventory.py http_firewall.yml

sleep 5


echo “Step 5: Configure and set up monitoring”
ansible-playbook -i generate_inventory.py monitoring9.yml

sleep 5

echo "Step 6: Mount and configure storage on all VMs"
ansible-playbook -i generate_inventory.py mount_storage.yml

sleep 5

echo "Step 7: Install Merizo on the worker VMs"
ansible-playbook -i generate_inventory.py install_merizo.yml

sleep 5

echo "Step 8: Download and extract datasets to shared storage"
ansible-playbook -i generate_inventory.py download_datasets.yml

sleep 5

echo “Step 9: Configure Redis”
ansible-playbook -i generate_inventory.py configure_redis.yml

echo "Step 10: Process the pipeline by setting up Redis and running tasks"
ansible-playbook -i generate_inventory.py process_pipeline.yml

sleep 15

echo “Step 11: Process Results”

ansible-playbook -i generate_inventory.py process_pipeline_results_2.yml

sleep 5

echo "Step 12: Running summary script/playbook"
ansible-playbook -i generate_inventory.py cath_summary.yml

sleep 5

echo "Step 13: Running full.yaml"
ansible-playbook -i generate_inventory.py full.yaml

sleep 5

echo "Step1 14: Opening ports for minio"
ansible-playbook -i generate_inventory.py open_minio_ports.yml

sleep 5

echo "Step 14: Setup MinIO"
ansible-playbook -i generate_inventory.py minio2.yml

sleep 5

echo "Step 15: Uploading data to MinIO"
ansible-playbook -i generate_inventory.py upload_minio.yml

sleep 5

echo "Step 16: Creating MinIO user"
ansible-playbook -i generate_inventory.py create_minio_user.yml

echo "Deployment and pipeline processing completed successfully!"
