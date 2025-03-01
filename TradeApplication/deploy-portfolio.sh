#!/usr/bin/env bash

# 1) Setting up the environment
echo "Starting deployment"
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com

# 2) Creating & uploading the image
docker build --platform linux/amd64 -t 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com/portfolio-service:latest -f Dockerfile.portfolio .  
docker push 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com/portfolio-service:latest

# 3) Cleanup
docker image 047719625934.dkr.ecr.ap-southeast-1.amazonaws.com/study-docker/nodea-app:latest