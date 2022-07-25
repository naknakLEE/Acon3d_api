from fastapi import APIRouter
from typing import Union

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/product")
def post_product():
    return {"Hello": "World"}

@router.get("/product")
def get_product():
    return {"Hello": "World"}

@router.put("/product")
def put_product():
    return {"Hello": "World"}
