from fastapi import APIRouter
from typing import Union

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}
