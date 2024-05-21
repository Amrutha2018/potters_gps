# GPS Tracking Microservices

This project consists of three microservices to handle GPS pings, process them via a worker service, and retrieve user track information. The services are containerized using Docker and managed with Docker Compose.

## Microservices

1. **GPS Ping API**: Accepts GPS pings and publishes them to RabbitMQ.
2. **Worker Service**: Processes the RabbitMQ queue and stores pings in PostgreSQL.
3. **User Track API**: Retrieves user track information based on a unique ID.

## Running the Application

### Prerequisites

- Docker
- Docker Compose

### Docker Compose Setup

To start the application, navigate to the project directory and run:

```sh
docker-compose up -d
```

### Accessing the Services
#### GPS Ping API (Port: 8002)

OpenAPI Documentation: http://localhost:8002/docs
#### Worker Service (Port: 8000)

This service does not expose an API for direct access but logs its activity. Check the logs for processing details.
#### User Track API (Port: 8001)

OpenAPI Documentation: http://localhost:8001/docs

### Viewing Docker Logs
```sh
docker-compose logs -f gps_ping_api
docker-compose logs -f worker_service
docker-compose logs -f user_track_api
```
