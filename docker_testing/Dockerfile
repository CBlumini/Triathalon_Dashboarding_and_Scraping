# Dockerfile
# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir dash

# Expose the port that the Dash app will run on
EXPOSE 8050

# Start the Dash app
CMD ["python", "app.py"]