
import numpy as np

from typing import Union
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import (
    HTTPBearer,
)

from utils.auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user)
from models.common import LoginForm, User, TokenData
from utils.db_connection import load_db, insert_db, load_product_db

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
security = HTTPBearer()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/token")
def post_product(
    form_data: LoginForm = Depends(),
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