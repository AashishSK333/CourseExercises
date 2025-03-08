#!/usr/bin/env bash

docker compose build --no-cache

docker compose up

# docker compose up -d  # Run in detached mode 

# docker compose logs -f
