create a single page web application for a trading feature for capital market. The web application is plugged with two python services for capturing the trade and the other service to display the portfolio of user account after trade execution. 


"Generate a structured project directory for a Flask-based single-page web application that provides two core features: Trade Capturing and Portfolio Management. These features should be served by two separate Python services. The application should be containerized using Docker and use PostgreSQL as the database. The directory should follow best practices for microservices architecture."

📌 Expected Output

/trade_service/ (Handles trade capture & stores trades in PostgreSQL)
/portfolio_service/ (Handles portfolio analytics & data retrieval)
/frontend/ (HTML, JavaScript for UI)
/docker-compose.yml (Defines multi-container setup)

"Create a Flask-based microservice called trade_service that provides RESTful APIs for capturing trades. It should have the following API endpoints:"

POST /trades → Accepts trade data (e.g., asset name, quantity, price, timestamp, trader ID) and stores it in PostgreSQL.
GET /trades/<trade_id> → Fetches trade details by ID.
GET /trades → Retrieves all trades with filtering options (e.g., by asset type or date).
📌 Requirements

Use Flask and Flask-RESTful
Connect to PostgreSQL using SQLAlchemy
Store trades in a trades table
Handle errors gracefully

"Create another Flask-based microservice called portfolio_service that provides RESTful APIs for portfolio management. It should support the following endpoints:"

GET /portfolio/<user_id> → Fetches a user's portfolio with aggregated trade details.
POST /portfolio/rebalance → Allows rebalancing of the portfolio based on predefined allocation rules.
📌 Requirements

Use Flask and Flask-RESTful
Fetch trade data from the trade_service using internal API calls
Compute portfolio values dynamically
Support JSON responses

"Define a PostgreSQL schema for storing trade data in a structured manner. Create a trades table with the following columns:"

trade_id (Primary Key, Auto-increment)
trader_id (Foreign Key)
asset_name (VARCHAR)
quantity (INTEGER)
price (DECIMAL)
trade_time (TIMESTAMP)

"Generate a simple HTML + JavaScript frontend that allows users to enter trade details and view their portfolio. The frontend should use Fetch API to communicate with the Flask backend services (trade_service and portfolio_service)."

📌 Key Features

A trade capture form (fields: asset name, quantity, price, timestamp, trader ID)
A portfolio summary dashboard fetching data from /portfolio/<user_id>

"Create a Dockerfile for each Flask microservice (trade_service and portfolio_service). Use Python 3.9, install dependencies via requirements.txt, and expose the required ports. Also, generate a docker-compose.yml to orchestrate the services along with a PostgreSQL container."

📌 Expected Files

trade_service/Dockerfile
portfolio_service/Dockerfile
docker-compose.yml (Defines Flask services, PostgreSQL, and networking)

my_flask_app/
├── trade_service/
│   ├── app.py
│   ├── models.py
│   ├── resources.py
│   ├── requirements.txt
│   └── Dockerfile
├── portfolio_service/
│   ├── app.py
│   ├── models.py
│   ├── resources.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── docker-compose.yml

# Connect to postgres container
docker exec -it <container_name_or_id> bash

# Once inside the container, connect to the database
psql -U user -d trades

# Connection established
-- List all tables
\dt

-- Show table structure
\d trade

-- Query all trades
SELECT * FROM trade;

-- Count trades
SELECT COUNT(*) FROM trade;

-- Find trades by trader_id
SELECT * FROM trade WHERE trader_id = 1;

-- Check database connection info
\conninfo

-- Exit psql
\q