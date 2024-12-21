from typing import Optional, Annotated
from schemas import users as user_schema
from db.db import async_session
from services.users import users_crud
from fastapi import Request, HTTPException, status
import random
from fastapi import Security, Depends, FastAPI
from fastapi.security.api_key import APIKeyHeader

from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")

class Token(BaseModel):
    token: str


#класс генерирует и хранит токены вместе со связанынми логинами
class AuthTokenController:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthTokenController, cls).__new__(cls)
            cls._instance.active_tokens = {}
        return cls._instance
    
    def get_new_token(self, login):
        token = 'token_'+str(random.randint(1,99999999))
        self.active_tokens[token] = login
        return token
    
    def get_username(self, token):
        return self.active_tokens[token]
    
    def check_token(self,token):
        return token in self.active_tokens


#проверка токена
async def verify_authorization(Authorization : Annotated[str, Depends(oauth2_scheme)]):
    try:
        print(Authorization )
        #headers = request.headers
        token = Authorization 
        token_is_active = AuthTokenController().check_token(token)
        if token_is_active:
            return AuthTokenController().get_username(token)
        return None
    except Exception as e:
        pass
    return None