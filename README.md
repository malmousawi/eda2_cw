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


# If you want to ssh into one of the machines:

Step 1:

cd /home/almalinux/ds4eng-infra/cnc-environment

Step 2:

ssh -i ssh_key_1.pem almalinux@10.134.12.xxx


# If you want to run the system from the already existing machine

Step 1:

tmux new -s test2

Step 2:

cd /home/almalinux/ds4eng-infra/cnc-environment

Step 3:

sudo chmod +x master_script_2.sh

Step 4:

./master_script_2.sh


