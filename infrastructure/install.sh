#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose python3 awscli
sudo usermod -aG docker ${USER}
echo ""
echo "Done!"