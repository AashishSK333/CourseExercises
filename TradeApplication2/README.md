Ensure no other processes are using ports 5001 and 5002.
    sudo lsof -i :5001
    sudo lsof -i :5002

sudo kill -9 <PID>

Kill all existing containers (if any).
    docker-compose down
    docker rm -f $(docker ps -aq) 

Rebuild and run the services.
    docker-compose down
    docker-compose build --no-cache
    docker-compose up
    # docker-compose up --build

Test the services in a new terminal window.

Test portfolio service:
curl http://localhost:5001/health

Test order service:
curl http://localhost:5002/health

Create an order:
    curl -X POST http://localhost:5002/orders -H "Content-Type: application/json" -d '{"user_id": "123", "order_type": "buy", "amount": 100}'
Check portfolio:
    curl http://localhost:5001/portfolios/123

Check Container Logs
    Check the logs of the order-service container to see if there are any errors.
        docker logs <order-service-container-id>
