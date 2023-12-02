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