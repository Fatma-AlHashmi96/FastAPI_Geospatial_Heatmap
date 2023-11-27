
from starlette.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Request, Response, Form
from pydantic import BaseModel
from typing import Optional
# import models
from sqlalchemy.orm import Session
# from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import  JWTError
import jwt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import ldap3
import logging

logging.basicConfig(level=logging.INFO) # Get the login information from server


app=FastAPI()
# Based on the key get the secrete authentication using SSO integartion with active directory
secret_key = "9iMo9N9mxB5aZWLyZZbM0Dryz_H3YQlue0bnXtLKuBk"
# Constants and Templates
ALGORITHM = "HS256"
templates = Jinja2Templates(directory="templates")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# Router Configuration
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


# LDAP Authentication
def authenticate_user_ldap(username: str, password: str):
    server = ldap3.Server('ldaps://ALHASHMI:636', get_info=ldap3.ALL)
    user_dn = f"CN={username},OU=users,DC=yourdomain,DC=com"
    try:
        with ldap3.Connection(server, user=user_dn, password=password) as conn:
            return conn.bind()
    except ldap3.core.exceptions.LDAPException:  
        return False

def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, secret_key, algorithm=ALGORITHM)

async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            await logout(request)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Not found")

@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user_ldap(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token_expires = timedelta(minutes=60)
    token = create_access_token(form_data.username, 1, expires_delta=token_expires)  # Assuming user ID 1 for example
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True

@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request):
    logging.debug(f"Request data: {await request.form()}")
    try:
        form = LoginForm(request)
        await form.create_oauth_form()

        # Authenticate using LDAP
        if not authenticate_user_ldap(form.username, form.password):
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

        # Create access token and set cookie
        token_expires = timedelta(minutes=60)
        token = create_access_token(form.username, 1, expires_delta=token_expires)  # Assuming user ID 1 for example
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response

    except Exception as e:
        logging.error(f"Login error: {e}")
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response

app.include_router(router)

