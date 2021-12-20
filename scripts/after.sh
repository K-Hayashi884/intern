#!/bin/bash
cd /home/ubuntu/intern-aws
sudo chown -R $USER /home/ubuntu/intern/postgres_data
docker-compose up --build