# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the shared library source files
COPY ../shared_lib /app/shared_lib/

# Copy the current directory contents into the container at /app
COPY user_track_api/app /app

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["sh", "-c", "PYTHONPATH=/app uvicorn main:app --host 0.0.0.0 --port 8001"]
