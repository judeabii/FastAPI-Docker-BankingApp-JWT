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
JSON Web Tokens (JWT) are a compact, URL-safe means of representing claims between two parties. In the context of this 
project, JWT tokenization refers to the process of generating and validating JWTs to enhance authentication and secure data exchange.
- **Token Generation:** Create JWTs with user information and expiration time.
- **Token Verification:** Validate incoming JWTs, ensuring their integrity and authenticity.
- **User Authentication:** Use JWTs to authenticate users and authorize access to protected endpoints.

```commandline
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
```

`create_access_token` function generates an access token based on input data. It creates a payload containing user data, 
adds an expiration time, and encodes it into a JSON Web Token (JWT) using the provided secret key and algorithm.

```commandline
def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)], credentials_exception):
    try:
        if token in auth.invalidated_tokens:
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("email")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_email
```
`verify_access_token` checks if a given token is valid by decoding it using the secret key and algorithm.

It also checks if the token is present in the list of invalidated tokens (from the auth module) to ensure tokens are not used after being invalidated.

### MongoDB transactions
To make a bank transfer, changes have to made to both the sender account 
and receiver account
```commandline
accounts_collection.update_one(
            {"account_number": senderAccount},
            {
                "$inc": {"balance": -amount},
                "$push": {"transfers_complete": transfer_id},
            })
        accounts_collection.update_one(
            {"account_number": accountNumber},
            {
                "$inc": {"balance": amount},
                "$push": {"transfers_complete": transfer_id},
            })
```
## Usage of FastAPI
1. Modern Web Development:
Embrace FastAPI's modern approach to web development, leveraging Python type hints for automatic data validation.
Benefit from asynchronous support, enhancing concurrency and scalability compared to traditional synchronous frameworks.
2. Fast and Predictable:
Leverage FastAPI's exceptional performance, surpassing traditional Python frameworks like Flask.
Enjoy predictable behavior, simplifying debugging and maintenance.