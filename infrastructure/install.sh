#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose python3 awscli
sudo usermod -aG docker ${USER}
aws --debug s3 cp s3://nefesh-artfacts/dags/ingestion_dados_publicos.py /home/hadoop/python/
echo ""
echo "Done!"