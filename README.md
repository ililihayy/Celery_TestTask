# Celery Users Fetch

A Flask application demonstrating asynchronous task processing with Celery and MongoDB.

## Overview

This project is a simple Flask application that fetches and stores user data from external APIs. It uses Celery to handle these operations asynchronously, MongoDB for data storage, and RabbitMQ as the message broker.

## Features

- Flask API for accessing stored user data
- Asynchronous data fetching using Celery tasks
- Data sources integration:
  - User data from JSONPlaceholder
  - Random address data from Random Data API
  - Random credit card data from Random Data API
- Containerized application with Docker and Docker Compose

## Tech Stack

- Python
- Flask
- Celery
- MongoDB
- RabbitMQ
- Docker & Docker Compose

## Project Structure

```
Celery_TestTask/
├── app/                    # Application code
│   ├── __pycache__/
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── db.py               # Database connections
│   └── tasks.py            # Celery tasks
├── templates/              # HTML templates
│   └── index.html
├── tests/                  # Test files
│   ├── __pycache__/
│   ├── test_fetch_addresses.py
│   ├── test_fetch_credit_cards.py
│   └── test_fetch_users.py
├── .codespellrc            # Code spell checking config
├── .env                    # Environment variables
├── .gitignore
├── .pre-commit-config.yaml # Pre-commit hooks
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── main.py                 # Flask application entry point
├── mypy.ini                # Type checking config
├── README.md
├── requirements.txt        # Python dependencies
├── ruff.toml               # Linting configuration
└── typos.toml              # Typo checking configuration
```

## Installation and Setup

### Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/ililihayy/Celery_TestTask.git
   cd Celery_TestTask
   ```

2. Start the application with Docker Compose:

   ```bash
   docker-compose up -d
   ```

3. The application will be available at:
   - Web interface: http://localhost:5000
   - RabbitMQ Management: http://localhost:15672 (guest/guest)

### Manual Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ililihayy/Celery_TestTask.git
   cd Celery_TestTask
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up MongoDB (required for data storage):

   ```bash
   # Install MongoDB on your system or use Docker
   docker run -d -p 27017:27017 --name mongodb mongo:6
   ```

5. Set up RabbitMQ (required for Celery):

   ```bash
   # Install RabbitMQ on your system or use Docker
   docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq rabbitmq:3-management
   ```

6. Start the Flask application:

   ```bash
   python main.py
   ```

7. Start the Celery worker:
   ```bash
   celery -A app.tasks worker --loglevel=info
   ```

## API Endpoints

### Main Page

```
GET /
```

Returns the main HTML page.

### Fetch All Data

```
GET /fetch-all
```

Triggers asynchronous tasks to fetch users, addresses, and credit cards data.

### Get Users

```
GET /users
```

Returns all users data stored in the database.

### Get Addresses

```
GET /addresses
```

Returns all addresses data stored in the database.

### Get Credit Cards

```
GET /credit-cards
```

Returns all credit cards data stored in the database.

## Celery Tasks

The application includes the following Celery tasks:

1. `fetch_users`: Fetches user data from JSONPlaceholder API
2. `fetch_addresses`: Fetches random address data for each user
3. `fetch_credit_cards`: Fetches random credit card data for each user
4. `fetch_all`: Helper function that triggers all three tasks above

## Database Structure

The application uses MongoDB with the following collections:

1. `users`: Stores user information
2. `addresses`: Stores address information linked to users by `uid`
3. `credit_cards`: Stores credit card information linked to users by `uid`

## Development

### Running Tests

The project includes tests for each data fetching task:

```bash
PYTHONPATH=. pytest tests/ # for Linux
```

```bash
$env:PYTHONPATH = (Get-Location); pytest tests/ # for Windows
```

### Linting and Formatting

The project includes configuration for:

- Ruff (linting)
- MyPy (type checking)
- Pre-commit hooks
