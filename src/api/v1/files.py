from fastapi import APIRouter, Header
from fastapi.responses import HTMLResponse
from typing import Any, List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from  schemas import files as file_schema
from db.db import get_session, async_session
from services.file_repository import file_crud
from services.utils import execution_controller
from services.auth import verify_authorization,oauth2_scheme
# Объект router, в котором регистрируем обработчики
router = APIRouter()



#Информация о загруженных файлах
@execution_controller
@router.get("/")
async def get_files(
    *,
    db: AsyncSession = Depends(get_session),
    username = Depends(verify_authorization),
) -> Any:
    #запрет использования без авторизации           
    if not username: return HTMLResponse(None, status_code=status.HTTP_403_FORBIDDEN)
    files = await file_crud.get_multi(db=db, username=username)
    return {
        "account_id":username,
        "files":files
    }


from fastapi.responses import HTMLResponse
#Загрузить файл в хранилище
@execution_controller
@router.post("/upload")
async def upload_file(
    *,
    db: AsyncSession = Depends(get_session),
    file_data: file_schema.FileBase,
    username = Depends(verify_authorization),
) -> Any:

    if not username: return HTMLResponse(None, status_code=status.HTTP_403_FORBIDDEN)

    #проверка на права записи в уже созданный файл, если такой есть
    has_access = file_crud.has_access_to_file(db, file_data.path, username)
    if not has_access: return HTMLResponse(None, status_code=status.HTTP_403_FORBIDDEN)
    
    #если такой файл уже есть в бд, удалить запись
    existing_url_record = await file_crud.get(db, file_data.path)
    if existing_url_record:
        await file_crud.delete(db, existing_url_record.id)

    file_record = await file_crud.create(db=db, obj_in=file_data, username=username)
    
    return file_record


#переадресация по короткой ссылке
@execution_controller
@router.get("/download")
async def download_file(
    *,
    db: AsyncSession = Depends(get_session),
    path: str, username = Depends(verify_authorization),
) -> Any:
    
    existing_url_record = await file_crud.get(db, path)
    if not existing_url_record:
        try:
            existing_url_record = await file_crud.get_by_id(db, int(path))
        except Exception as e:
            pass

    if not existing_url_record: return HTMLResponse(None, status_code=status.HTTP_404_NOT_FOUND)

    with open(existing_url_record.path) as f_in:
        return '\n'.join(f_in.readlines())

