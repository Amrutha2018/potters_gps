import aio_pika
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from api import process_message
from contextlib import asynccontextmanager
from aio_pika.exceptions import AMQPConnectionError, ChannelClosed
from urls import router as worker_router 
from logging_config import logger

# Create FastAPI instance
app = FastAPI(
    title="Worker Service",
    description="Service for processing GPS pings from RabbitMQ",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root URL to verify service is running
@app.get("/")
async def read_root():
    logger.info("Worker service is running")
    return {"message": "Worker service is running"}

app.include_router(worker_router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception for request {request.url}: {exc}", exc_info=True)
    return HTTPException(status_code=500, detail="Internal Server Error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to RabbitMQ and setup channel and queue
    try:
        logger.info("Connecting to RabbitMQ")
        connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
        logger.info("Successfully connected to RabbitMQ")

        channel = await connection.channel()
        logger.info("RabbitMQ channel created")

        queue = await channel.declare_queue("gps_pings", durable=True)
        logger.info("RabbitMQ queue declared")

        await queue.consume(process_message, no_ack=False)
        logger.info("Worker started and consuming messages from RabbitMQ")

        app.state.connection = connection
        app.state.channel = channel

        yield

    except AMQPConnectionError as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to RabbitMQ")
    except ChannelClosed as e:
        logger.error(f"Failed to create RabbitMQ channel: {e}")
        raise HTTPException(status_code=500, detail="Failed to create RabbitMQ channel")
    except Exception as e:
        logger.error(f"An error occurred during startup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred during startup")

    # Shutdown: Close RabbitMQ connection
    try:
        logger.info("Shutting down RabbitMQ connection")
        await app.state.connection.close()
        logger.info("RabbitMQ connection closed")
    except Exception as e:
        logger.error(f"An error occurred during shutdown: {e}", exc_info=True)

# Attach lifespan event handlers to the app
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)