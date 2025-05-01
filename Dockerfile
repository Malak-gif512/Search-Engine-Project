# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy all the project files into the container
COPY . /app/

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the app using uvicorn
CMD exec uvicorn main_fastapi:app --host 0.0.0.0 --port ${PORT}

