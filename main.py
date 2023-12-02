from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from routers import auth, transfer

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(transfer.router)


@app.get("/", response_class=HTMLResponse)
def home_page():
    return RedirectResponse('/login', status_code=302)


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        # Render a custom HTML page for unauthorized access
        return templates.TemplateResponse("logout.html", {"request": request})
    return exc
