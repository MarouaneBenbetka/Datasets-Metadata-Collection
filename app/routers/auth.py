from fastapi import APIRouter, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
from ..db_config import run_query
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.utils.jwt import get_password_hash, verify_password, create_access_token
import jwt


router = APIRouter()


class UserCredentials(BaseModel):
    username: str
    password: str


@router.post("/register/")
def register(credentials: UserCredentials):
    username = credentials.username
    password = credentials.password

    if not username or not password:
        raise HTTPException(
            status_code=400, detail="Username and password are required")

    hashed_password = get_password_hash(password)
    try:
        run_query("INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
                  (username, hashed_password))

        token = create_access_token(username)
        return {"username": username, "accessToken": token, "message": "User registered successfully"}
    except:
        raise HTTPException(
            status_code=400, detail="Username is already in use")


@router.post("/login/")
def login(credentials: UserCredentials):
    username = credentials.username
    password = credentials.password

    if not username or not password:
        raise HTTPException(
            status_code=400, detail="Username and password are required")

    db_users = run_query(
        f"SELECT * FROM users WHERE username = '{username}' limit 1")

    user = db_users[0]
    if not user or not verify_password(password, user['hashed_password']):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    accessToken = create_access_token(username)
    return {"username": user['username'], "accessToken": accessToken, "message": "Login successful"}
