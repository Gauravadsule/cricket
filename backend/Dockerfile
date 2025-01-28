# Use Python 3.8 as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the backend application code into the container
COPY backend/ /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Set environment variables to disable buffering of output
ENV PYTHONUNBUFFERED=1

# Command to run the Flask app
CMD ["python", "app.py"]