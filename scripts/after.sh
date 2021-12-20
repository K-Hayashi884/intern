#!/bin/bash
cd /home/ubuntu/intern-aws
sudo chown -R $USER postgres_data
docker-compose up --build