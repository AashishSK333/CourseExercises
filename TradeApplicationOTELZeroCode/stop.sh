#!/usr/bin/env bash

docker compose down

docker rmi $(docker images -q)

docker volume rm $(docker volume ls -q)

docker network rm $(docker network ls -q)

# Remove any dangling volumes
#docker volume prune -f

# Clean up dangling images
#docker image prune -f

echo "Cleanup completed. You can now restart with ./start.sh"