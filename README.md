# FastAPI-Docker-BankingApp-JWT
Discover a sophisticated banking web application crafted with FastAPI, Docker, and JWT. This repository showcases the fusion of FastAPI for a robust backend, Docker for effortless deployment, and the trio of HTML, CSS and JavaScript for a dynamic web interface

### Steps to Install Docker
Install Docker

If you haven't installed Docker Desktop for Windows, follow the instructions in the official Docker documentation for Windows to download and install Docker.

###  Use MongoDB Docker Image

Enter the below code in the docker-compose.yml file to use the mongo DB Docker Image
```commandline
  mongo_db:
    container_name: db_container
    image: mongo:latest
    restart: always
    ports:
      - 2717:27017
    volumes:
      - mongo_db:/data/db
```
Mapping the container's port 27017 to the host machine's port 2717

### Dockerization of application code
```commandline
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 8000:8000
    volumes:
      - .:/app
    environment:
      MONGODB_URI: mongodb://mongo_db:2717
      DB_NAME: bank
    depends_on:
      - mongo_db
```
This is to be added into the docker-compose.yml file. The name of the container is `backend`
and can be accessed using port 8000.

We build the contents of the Dockerfile below to create and run the container:
```commandline
FROM python:3.9
WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
#### Command to run the containers
```commandline
docker compose up --build 
```
This command will start both the `backend` and `db_container` containers

## JWT Tokenization