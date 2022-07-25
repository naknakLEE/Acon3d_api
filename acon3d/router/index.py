from fastapi import APIRouter
from typing import Union

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    user_name: Union[str, None] = None
    user_role: Union[str, None] = None
    user_pwd: str



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
        return User(
            user_id = user_id,
            user_name = user_name,
            user_pwd = user_pwd,
            user_role = user_role
            )

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.user_pwd):
        return False
    return user


from datetime import datetime, timedelta
ACCESS_TOKEN_EXPIRE_MINUTES = 30
from jose import JWTError, jwt
import pandas as pd

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def load_db():
    df = pd.read_csv ('../db/user_db.csv')
    return df



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
def post_product(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_db = Depends(load_db)
):
    user = authenticate_user(user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/product")
def post_product():
    return {"Hello": "World"}

@router.get("/product")
def get_product():
    return {"Hello": "World"}

@router.put("/product")
def put_product():
    return {"Hello": "World"}
