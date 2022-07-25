import pandas as pd
import numpy as np

from typing import Union
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Security, APIRouter
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from models.common import LoginForm, User, TokenData
from utils.db_connection import load_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
security = HTTPBearer()


def verify_password(plain_password, hashed_password):
    res = True if plain_password == hashed_password else False
    print(res)
    return True if plain_password == hashed_password else False

def get_user(db, username: str):
    db = db.loc[db['user_id'] == username]
    
    if len(db) != 0:
        user_id = db['user_id'].to_string(index = False)
        user_name = db['user_name'].to_string(index = False)
        user_pwd = db['user_pwd'].to_string(index = False)
        user_role = db['user_role'].to_string(index = False)
        index = db['index'].to_string(index = False)
        return User(
            user_id = user_id,
            user_name = user_name,
            user_pwd = user_pwd,
            user_role = user_role,
            index = index
            )

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.user_pwd):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db = load_db()
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
