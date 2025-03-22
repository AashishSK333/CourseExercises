#!/usr/bin/env bash

# Check for AWS credentials
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
  echo "AWS credentials not found. Please set them up:"
  echo "export AWS_ACCESS_KEY_ID=your_access_key"
  echo "export AWS_SECRET_ACCESS_KEY=your_secret_key"
  echo "export AWS_REGION=ap-southeast-1"
  exit 1
fi

# Make sure AWS_REGION is set
if [ -z "$AWS_REGION" ]; then
  export AWS_REGION=ap-southeast-1
  echo "AWS_REGION not set, defaulting to ap-southeast-1"
fi

echo "AWS credentials detected, building instrumented services..."

# Build and start the application
docker compose -f docker-compose.yml build --no-cache
docker compose up



# docker compose up -d  # Run in detached mode 

# docker compose logs -f
