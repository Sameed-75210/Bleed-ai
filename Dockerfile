# Use the official Python image for Python 3.11
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Modify the requirements.txt to exclude 'pywin32' dynamically (if needed)
RUN sed -i '/pywin32/d' requirements.txt

# Install pip and any dependencies from modified requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create and activate virtual environment, and install dependencies
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["/bin/bash", "-c", "source venv/bin/activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000"]
