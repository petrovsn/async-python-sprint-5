


import base64
import os

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel

from sqlalchemy import func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.base import Base
from models.files import File
from schemas.files import FileCreate, FileUpdate


from .base import Repository

from fastapi.encoders import jsonable_encoder

from .repository import RepositoryDB

    #id = Column(Integer, primary_key=True)
    #url_full = Column(String)
    #url_short = Column(String)
    #created_at = Column(DateTime, server_default=func.now())
    #usage_counter = Column(Integer)
    #status = Column(String)


class RepositoryFile(RepositoryDB[File, FileCreate, FileUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: FileCreate, username: Any) -> File:
        obj_in_data = jsonable_encoder(obj_in)
        
        data_b64 = obj_in_data["data_b64"]
        path = obj_in_data["path"]

        #data_bytes  = base64.b85decode(data_b64)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(data_b64)


        obj_in_db = {}

        obj_in_db["path"] = obj_in_data["path"]
        obj_in_db["name"] = os.path.basename(path)
        obj_in_db["created_by"] = username
        obj_in_db["size"] = len(data_b64)
        obj_in_db["is_downloadable"] = True

        db_obj = self._model(**obj_in_db)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_multi(self, db: AsyncSession, username: str ) -> List[File]:
        statement = select(self._model).where(self._model.created_by == username)
        results = await db.execute(statement=statement)
        return results.scalars().all()
    
    async def get(self, db: AsyncSession, path: str) -> Optional[File]:
        statement = select(self._model).where(self._model.path == path)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()
    
    async def get_by_id(self, db: AsyncSession, id: Any) -> Optional[File]:
        statement = select(self._model).where(self._model.id == id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()
    
    async def has_access_to_file(self, db: AsyncSession, path: str, username:str):
        statement = select(self._model).where(self._model.path == path, self._model.created_by != username)
        results = await db.execute(statement=statement)
        results = results.scalars().all()
        if results:
            return False
        return True
    
    async def delete(self, db: AsyncSession, id: int):
        statement = delete(self._model).where(self._model.id == id)
        results = await db.execute(statement=statement)
        await db.commit()
        return None
    
    
    


file_crud = RepositoryFile(File) 


