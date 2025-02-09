#!/bin/bash

sudo chown -R almalinux:almalinux /home/almalinux/eda2_cw

# Install yum-utils (auto-approve)
echo "Installing yum-utils..."
sudo yum install -y yum-utils

echo "Installing tmux"
sudo dnf install -y tmux

# Add HashiCorp repo and install Terraform (auto-approve)
echo "Adding HashiCorp repo and installing Terraform..."
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

# Install EPEL repository and Ansible (auto-approve)
echo "Installing EPEL repository and Ansible..."
sudo yum install -y epel-release
sudo yum install -y ansible

# Move into the cnc-environment directory
echo "Navigating to the cnc-environment directory..."
cd /home/almalinux/ds4eng-infra/cnc-environment

echo "Setup complete!"
