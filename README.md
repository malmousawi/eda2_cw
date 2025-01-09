# eda1_cw

# These are the steps to run the coursework on a brand new fresh machine

Step 0:
sudo dnf install git

Step 1: 
git clone https://github.com/malmousawi/eda1_cw.git

Step 2:
cd /home/almalinux/eda1_cw

Step 3: 
chmod +x setup_environment.sh

Step 4:
./setup_environment.sh

Step 5:
cd /home/almalinux/ds4eng-infra/cnc-environment

Step 6:
tmux new -s test

tmux attach -t test (# run this if you deactivate from the tmux session)

Step 7:
sudo chmod +x master_script.sh

Step 8:
./master_script.sh
(when prompted to enter a username, dont enter 'ucabm68' as I have another machine with the same user name. I recommend 'ucab68')

# If you want to ssh into one of the machines:

Step 1:

cd /home/almalinux/ds4eng-infra/cnc-environment

Step 2:

ssh -i ssh_key_1.pem almalinux@10.134.12.xxx


# Current Machines:

username: IP Address

local: 10.134.12.10

ucab68-host-3fef47a8a7: 10.134.12.47

ucab68-worker-01-3fef47a8a7: 10.134.12.122

ucab68-worker-02-3fef47a8a7: 10.134.12.29

ucab68-worker-03-3fef47a8a7: 10.134.12.74

ucab68-storage-3fef47a8a7: 10.134.12.104


# If you want to run the system from the already existing machine

Step 1:

tmux new -s test2

Step 2:

cd /home/almalinux/ds4eng-infra/cnc-environment

Step 3:

sudo chmod +x master_script_2.sh

Step 4:

./master_script_2.sh


