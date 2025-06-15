# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# This includes your Python script (generate_electronics_page.py)
# and the 'web' directory it creates.
COPY . /app

# Expose port 8000, which is where our Python HTTP server will listen
EXPOSE 8000

# Command to run the Python script.
# This script will generate the index.html and then start the HTTP server.
CMD ["python", "generate_electronics_page.py"]
