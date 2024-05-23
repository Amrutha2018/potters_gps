# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install sed (if not already available)
RUN apt-get update && apt-get install -y sed

# Copy the shared library source files
COPY ../shared_lib /app/shared_lib/

# Copy the current directory contents into the container at /app
COPY worker_service/app /app

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait-for-it script
COPY worker_service/wait-for-it.sh /wait-for-it.sh
# RUN chmod +x /wait-for-it.sh
RUN sed -i 's/\r$//' /wait-for-it.sh && chmod +x /wait-for-it.sh

# Run the application
CMD ["sh", "-c", "/wait-for-it.sh rabbitmq:5672 -- && PYTHONPATH=/app uvicorn main:app --host 0.0.0.0 --port 8000"]
