# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code into the image
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Define the command to start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_network.wsgi:application"]
