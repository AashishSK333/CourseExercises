#!/usr/bin/env bash

docker compose -f docker-compose.yml build --no-cache

docker compose up

# docker compose up -d  # Run in detached mode 

# docker compose logs -f
