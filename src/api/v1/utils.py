from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import users as user_schema
from db.db import get_session
from services.users import users_crud
from services.file_repository import file_crud
from services.utils import execution_controller
# Объект router, в котором регистрируем обработчики
router = APIRouter()

#тестовый эндпойнт, проверяющий, что оно работает
@execution_controller
@router.get("/test/ep")
async def test_ep() -> Any:
    return "ok"

#Получить информацию о времени доступа ко всем связанным сервисам, например, к БД, кэшам, примонтированным дискам и т.д.
@execution_controller
@router.get("/ping", status_code=status.HTTP_200_OK)
async def get_ping():
    return "ok"


