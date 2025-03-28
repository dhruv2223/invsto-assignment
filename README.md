# FastAPI + PostgreSQL Docker Setup

This guide will help you set up and run the FastAPI application with a PostgreSQL database using Docker.

## Prerequisites

- Docker and Docker Compose installed

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/dhruv2223/invsto-assignment
cd invsto-assignment
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```sh
# PostgreSQL container environment variables
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@db/your_database_name
POSTGRES_PORT=5432

# FastAPI app database connection variables
DB_NAME=your_database_name
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=db  # Must match the service name in docker-compose.yml
DB_PORT=5432
```

### 3. Build and Run the Containers

```sh
docker-compose up --build
```

This will start the PostgreSQL database and the FastAPI application.

### 4. Access the Application

Once the containers are running:

- FastAPI will be available at: [http://localhost:8000](http://localhost:8000)
- PostgreSQL will be running on port `5432` inside the container.

### 5. Stopping the Containers

To stop the containers without removing data:

```sh
docker-compose down
```

To stop and remove all data:

```sh
docker-compose down -v
```

### 6. Running the App Without Docker (Optional)

If you want to run the FastAPI app without Docker:

```sh
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Make sure PostgreSQL is running locally and update the `.env` file accordingly.

For any issues, check the container logs using:

```sh
docker logs fastapi_app
```

---
