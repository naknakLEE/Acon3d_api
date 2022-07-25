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
    index: int
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

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from datetime import datetime, timedelta
ACCESS_TOKEN_EXPIRE_MINUTES = 30
from jose import JWTError, jwt
import pandas as pd

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def load_db():
    df = pd.read_csv ('../db/user_db.csv')
    return df

def load_product_db():
    df = pd.read_csv ('../db/acon3d_db.csv')
    return df

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import APIRouter, Depends, BackgroundTasks, Header, Security


class TokenData(BaseModel):
    username: Union[str, None] = None
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



def insert_db(data_df_2):
    try:
        data_df_2.to_csv('../db/acon3d_db.csv',
            sep=',',
            na_rep='NaN',
            float_format = '%.2f',
            index = False)
        return True
    except:
        return False
    

@router.post("/product")
def post_product(
    product_name: str,
    title_kr: str, 
    content_kr: str, 
    user: str = Depends(get_current_user)
    ):
    
    if user.user_role != '작가':
        return {"msg": "작가 권한이 없습니다."}
    p_dao = load_product_db()
    
    new_data = {
    'product_name' : product_name,
    'title_kr' : title_kr,
    'content_kr' : content_kr,
    "user_index" : int(user.index),
    "status": "검토 요청"
    }
    p_dao = p_dao.append(new_data, ignore_index=True)
    p_dao['index'] = p_dao.index

    if insert_db(p_dao):
        return {"msg": "상품 등록 성공"}

@router.get("/product")
def get_product(user: str = Depends(get_current_user)):
    if user.user_role != '에디터':
        return {"msg": "에디터 권한이 없습니다."}
    p_dao = load_product_db()
    p_dao = p_dao.loc[p_dao['status'] == "검토 요청"]
    
    res = {}
    
    rows = []
    
    for index, row in p_dao.iterrows():
        rows.append({'product_index' : row['index'],
                    'product_name' : row['product_name'],
                    'title_kr' : row['title_kr'],
                    'content_kr' : row['content_kr'],
                    'user_index' : row['user_index'],
                    'status' : row['status'],})
    res["msg"] = rows
    return res

@router.put("/product")
def put_product(
                product_index: int,
                title_kr: str,
                content_kr: str,
                title_en: str,
                content_en: str,
                title_cn: str,
                content_cn: str,
                price: float,
                tax: float,
                user: str = Depends(get_current_user),
                ):
    if user.user_role != '에디터':
        return {"msg": "에디터 권한이 없습니다."}
    p_dao = load_product_db()
    check_p_dao = p_dao.loc[p_dao['index'] == product_index]
    if len(check_p_dao) == 0:
        return{"msg" : "상품이 존재하지 않습니다."}
    
    p_dao.at[product_index,'title_kr']=title_kr
    p_dao.at[product_index,'content_kr']=content_kr
    p_dao.at[product_index,'title_en']=title_en
    p_dao.at[product_index,'content_en']=content_en
    p_dao.at[product_index,'title_cn']=title_cn
    p_dao.at[product_index,'content_cn']=content_cn
    p_dao.at[product_index,'price']=price
    p_dao.at[product_index,'tax']=tax
    p_dao.at[product_index,'status']="검토 완료"
    
    if insert_db(p_dao):
        return {"msg": "상품 등록 성공"}
    else:
        return {"msg": "상품 업데이트 실패"}
    
    
    
import json
import simplejson

from fastapi.encoders import jsonable_encoder
import orjson

# class ORJSONResponse(JSONResponse):
#     media_type = "application/json"

#     def render(self, content) -> bytes:
#         return orjson.dumps(content)

import numpy as np
@router.get("/list/product")
def get_list_product():
    p_dao = load_product_db()
    p_dao = p_dao.loc[p_dao['status'] == "검토 완료"]
    
    res = {}
    
    rows = []
    
    for index, row in p_dao.iterrows():
        row = row.replace(np.nan,0)
        rows.append({'product_index' : row['index'],
                    'product_name' : row['product_name'] if row['product_name'] else None,
                    'title_kr' : row['title_kr'] if row['title_kr'] else None,
                    'content_kr' : row['content_kr'] if row['content_kr'] else None,
                    'title_en' : row['title_en'] if row['title_en'] else None,
                    'content_en' : row['content_en'] if row['content_en'] else None,
                    'title_cn' : row['title_cn'] if row['title_cn'] else None,
                    'content_cn' : row['content_cn'] if row['content_cn'] else None,
                    'price' : row['price'] if row['price'] else 0,
                    'tax' : row['tax'] if row['tax'] else 0,
                    'user_index' : row['user_index'] if row['user_index'] else 0,
                    'status' : row['status'],})
    res["msg"] = rows
    return res