#!/bin/bash
curl -o /home/ubuntu/airflow/dags/nefesh_pipeline.py https://nefesh-artfacts.s3.us-east-2.amazonaws.com/dags/nefesh_pipeline.py 
cd /home/ubuntu/airflow/
astro dev start
echo ""
echo "Done!"