# Use the official Python image from the Docker Hub
FROM python:3.11.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code into the container
COPY . .

# Specify the command to run your application
# Replace 'app.py' with the file you want to run
CMD ["python", "app.py"]
