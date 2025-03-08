#!/usr/bin/env bash

# 1) Setting up the environment
echo "Starting deployment"
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com

# Ensure the templates and static directories exist
mkdir -p templates
mkdir -p static

# 2) Creating & uploading the image
docker build --platform linux/amd64 -t 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com/order-service:latest -f Dockerfile.order .  
docker push 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com/order-service:latest

# 3) Cleanup
docker rmi 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com/order-service:latest