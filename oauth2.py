from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime,timedelta
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.templating import Jinja2Templates
from routers import auth
from dotenv import load_dotenv
import os
templates = Jinja2Templates(directory="templates")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


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


def get_current_user(token: Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
