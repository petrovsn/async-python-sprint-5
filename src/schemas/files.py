from typing import Optional
from datetime import datetime

from pydantic import BaseModel

# Shared properties
class FileBase(BaseModel):
    data_b64: str
    path: str

# Properties to receive on File creation
class FileCreate(FileBase):
    pass

# Properties to receive on File update
class FileUpdate(BaseModel):
    pass

# Properties shared by models stored in DB
class FileInDBBase(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: str
    path: str
    size: int
    is_downloadable: bool

# Properties to return to client
class File(FileInDBBase):
    pass

# Properties stored in DB
class FileInDB(FileInDBBase):
    pass 