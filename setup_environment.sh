#!/bin/bash

# Clone the repositories
echo "Cloning repositories..."
git clone https://github.com/owainkenwayucl/ds4eng-infra.git

# Copy files from eda1_cw to ds4eng-infra
echo "Copying files..."
sudo cp -r /home/almalinux/eda1_cw/* /home/almalinux/ds4eng-infra/cnc-environment

# Install yum-utils (auto-approve)
echo "Installing yum-utils..."
sudo yum install -y yum-utils

# Add HashiCorp repo and install Terraform (auto-approve)
echo "Adding HashiCorp repo and installing Terraform..."
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

# Install EPEL repository and Ansible (auto-approve)
echo "Installing EPEL repository and Ansible..."
sudo yum install -y epel-release
sudo yum install -y ansible

# Change ownership of the ds4eng-infra/cnc-environment directory
echo "Changing ownership of the ds4eng-infra/cnc-environment directory..."
sudo chown -R almalinux:almalinux /home/almalinux/ds4eng-infra/cnc-environment

# Move into the cnc-environment directory
echo "Navigating to the cnc-environment directory..."
cd /home/almalinux/ds4eng-infra/cnc-environment

echo "Setup complete!"
