from typing import Union
from pydantic import BaseModel
from fastapi import Form


class LoginForm:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...)
    ):
        self.username = username
        self.password = password
        
class User(BaseModel):
    index: int
    user_id: str
    user_name: Union[str, None] = None
    user_role: Union[str, None] = None
    user_pwd: str

class TokenData(BaseModel):
    username: Union[str, None] = None
