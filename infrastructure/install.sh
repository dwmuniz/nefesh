#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose python3 awscli
sudo usermod -aG docker ${USER}
curl -sSL https://install.astronomer.io | sudo bash
mkdir /home/ubuntu/airflow/
cd /home/ubuntu/airflow/
astro dev init
curl -o /home/ubuntu/airflow/dags/nefesh_pipeline.py https://nefesh-artfacts.s3.us-east-2.amazonaws.com/dags/nefesh_pipeline.py 
echo ""
echo "Done!"