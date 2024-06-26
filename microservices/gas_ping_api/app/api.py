from fastapi import HTTPException
import json
from shared_lib.schemas import GpsPingCreate
from logging_config import logger
import aio_pika
from aio_pika.exceptions import AMQPConnectionError, ChannelClosed


async def receive_gps_ping(ping: GpsPingCreate):
    """
    Receive a GPS ping and publish it to RabbitMQ.

    - **ping**: The GPS ping data including latitude, longitude, timestamp, and user ID.
    - **response**: Returns the received ping data on successful publishing to RabbitMQ.
    """
    logger.info("Received a new GPS ping")
    try:
        # Connect to RabbitMQ
        try:
            logger.info("Attempting to connect to RabbitMQ")
            connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
            logger.info("Successfully connected to RabbitMQ")
        except AMQPConnectionError as conn_err:
            logger.error(f"RabbitMQ connection error: {conn_err}")
            raise HTTPException(status_code=500, detail="Error connecting to RabbitMQ")

        try:
            channel = await connection.channel()
            logger.info("RabbitMQ channel created")
        except ChannelClosed as chan_err:
            logger.error(f"RabbitMQ channel creation error: {chan_err}")
            await connection.close()
            raise HTTPException(status_code=500, detail="Error creating RabbitMQ channel")

        # Prepare the message payload
        message_body = ping.dict()
        # Convert the datetime to a string
        if 'timestamp' in message_body:
            message_body['timestamp'] = message_body['timestamp'].isoformat()

        try:
            # Publish the message to RabbitMQ
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message_body).encode()),
                routing_key="gps_pings"
            )
            logger.info("Successfully published message to RabbitMQ")
        except Exception as pub_err:
            logger.error(f"Error publishing message to RabbitMQ: {pub_err}")
            raise HTTPException(status_code=500, detail="Error publishing message to RabbitMQ")
        finally:
            await connection.close()
            logger.info("RabbitMQ connection closed")

        return ping

    except HTTPException as http_exc:
        raise http_exc  # Re-raise HTTP exceptions to be handled by FastAPI

    except Exception as e:
        logger.error(f"Unhandled error processing GPS ping: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
