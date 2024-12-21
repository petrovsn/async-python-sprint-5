from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import users as user_schema
from db.db import get_session
from services.users import users_crud
from services.utils import execution_controller
from services.auth import AuthTokenController

# Объект router, в котором регистрируем обработчики
router = APIRouter()

#Регистрация нового пользователя. Запрос принимает на вход логин и пароль для создания новой учетной записи.
@execution_controller
@router.post(
    "/register", status_code=status.HTTP_200_OK  #response_model=file_schema.File, 
)
async def create_user(
    *,
    db: AsyncSession = Depends(get_session),
    entity_in: user_schema.UserCreate,
) -> Any:
    # create item by params
    entity = await users_crud.create(db=db, obj_in=entity_in)
    return entity


#Авторизация пользователя
@execution_controller
@router.post("/auth")
async def auth_user(
    *,
    db: AsyncSession = Depends(get_session),
    entity_in: user_schema.UserCreate
) -> Any:
    
    is_user_exist = await users_crud.verify(db,entity_in.login, entity_in.password)
    if not is_user_exist:
        return HTMLResponse(None,status.HTTP_403_FORBIDDEN)
    
    token = AuthTokenController().get_new_token(entity_in.login)
    return {"access_token":token}













