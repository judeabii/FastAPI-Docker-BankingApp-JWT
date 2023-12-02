from fastapi import FastAPI, Request, Header, Depends, HTTPException, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime
from random import randint
from database import user_collection, accounts_collection
import oauth2

router = APIRouter()
templates = Jinja2Templates(directory="templates")

invalidated_tokens = set()


@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/user', response_class=HTMLResponse)
def user_login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends()):
    print(user_credentials.username)
    result = user_collection.find_one({"name": user_credentials.username}, {"name": True, "password": True,
                                                                            "email": True})
    if result is None or result['password'] != user_credentials.password:
        return RedirectResponse('/login', status_code=303)
    else:

        access_token = oauth2.create_access_token(data={"email": result['email']})
        print(access_token)
        result2 = accounts_collection.find_one({"email": result['email']})
        data = result2
        response = templates.TemplateResponse("home.html", {"request": request, "data": data})
        response.set_cookie(key="access_token", value=access_token)
        response.set_cookie(key="token_type", value="bearer")

        return response


@router.get('/register')
def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post('/register', response_class=HTMLResponse)
def user_register(username: Annotated[str, Form()], password: Annotated[str, Form()],
                  email: Annotated[str, Form()], request: Request):
    print(f'{username} {password} {email}')
    existing_user = user_collection.find_one({"email": email})
    if existing_user:
        print("error")
        data = {
            "error": "User with this email is already registered"
        }
        return templates.TemplateResponse("register.html", {"request": request, "error": data})
    else:
        acc_number = randint(10000000, 99999999)
        new_user = {
            "name": username,
            "password": password,
            "email": email,
            "created_on": datetime.now()
        }
        new_account = {
            "name": username,
            "email": email,
            "account_type": "Savings",
            "balance": 1000,
            "account_number": acc_number,
            "last_updated": datetime.now()
        }
        result1 = user_collection.insert_one(new_user)
        doc_id = result1.inserted_id

        result2 = accounts_collection.insert_one(new_account)
        doc_id2 = result2.inserted_id

        return RedirectResponse('/login', status_code=302)


@router.post('/logout')
def logout_page(request: Request, authorization: str = Header(...),
                current_user: str = Depends(oauth2.get_current_user)):
    scheme, token = authorization.split()
    print(current_user)
    invalidated_tokens.add(token)
    return templates.TemplateResponse("logout.html", {"request": request})
