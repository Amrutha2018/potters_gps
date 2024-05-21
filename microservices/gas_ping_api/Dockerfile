# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the shared library
COPY ../shared_lib /app/shared_lib

# Copy the requirements.txt file
COPY gas_ping_api/app/requirements.txt /app/

# Copy the current directory contents into the container at /app
COPY gas_ping_api/app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
