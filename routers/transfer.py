from fastapi import FastAPI, Request, Depends, status, HTTPException, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from datetime import datetime
from random import randint
import oauth2
from database import user_collection, accounts_collection


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/transfer')
def simulate_transfer(senderAccount: Annotated[int, Form()],
                      accountNumber: Annotated[int, Form()], amount: Annotated[float, Form()],request: Request,
                      get_current_user: int = Depends(oauth2.get_current_user)):
    print(get_current_user)
    if senderAccount == accountNumber:
        error = {
            "error": "You cannot transfer money to yourself!"
        }
        data = {
            "account_number": senderAccount
        }
        return templates.TemplateResponse("home.html", {"request": request, "error": error, "data": data})
    else:
        transfer_id = "TR" + str(randint(100000, 999999))
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
        success = {
            "msg": f"You have successfully transferred Rs.{amount} to the Account: {accountNumber}"
        }
        data = {
            "account_number": senderAccount
        }
        return templates.TemplateResponse("home.html", {"request": request, "success": success, "data": data})
