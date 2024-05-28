# Bleed-ai

# Loom Video Demonstrating the functionalities of FastAPI application:

https://www.loom.com/share/b8a146ea5b064e32bb150d1ed55393ae


## FastAPI User Management and Image Processing Application

This repository contains a FastAPI application designed to demonstrate user management functionalities including authentication, and image processing capabilities using MediaPipe for face detection.

## Features
- **Database Operations**: Design and interaction with a user database using SQLAlchemy ORM.
- **API Management**: Robust endpoint configurations using FastAPI.
- **Machine Learning Operations**: Integration of MediaPipe for facial detection in images.
- **Deployment**: Containerization with Docker for easy deployment and scalability.

## Prerequisites
You need Python 3.11+ installed on your local development machine.

## Installing
Clone the repository to your local machine:

    git clone https://github.com/yourusername/yourrepositoryname.git

## Create and Activate a Virtual Environment

It's recommended to create a virtual environment to manage the dependencies for your project separately. You can create and activate a virtual environment using:

For Windows:

    python -m venv venv
    \venv\Scripts\activate
    
For macOS and Linux:

    python3 -m venv venv
    source venv/bin/activate

Install the required dependencies:

    pip install -r requirements.txt


## Running the application
Start the FastAPI server by running:

    uvicorn app:app --reload

## Docker Setup

Ensure Docker is installed on your system. If you are using Windows, it is recommended to enable WSL2 for optimal performance.

## Pull the image from Docker Hub:

    bash docker pull sameed75210/bleedai-project:latest

## Run the container:

    bash docker run -d -p 8000:8000 sameed75210/bleedai-project:latest

## API Endpoints
Here is an overview of the key API endpoints available in this application:

- **POST /create:** Create a new user.
- **GET /{user_id}:** Retrieve a user's name by their ID.
- **PUT /{user_id}:** Update a user's name by their ID.
- **POST /search:** Search for users by name.
- **POST /process_image:** Upload an image for facial detection.

## Contributing

I welcome contributions to the BleedAI project! If you have suggestions or improvements, please follow these steps:

- Fork the repository.
- Create a new branch

    ```git checkout -b feature-branch```

- Make your changes.
- Commit your changes
  
  ```git commit -am 'Add some feature'```
- Push to the branch
  
  ``` git push origin feature-branch```
- Create a new Pull Request.
