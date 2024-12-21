from models.Files import File as FileModel
from .repository import RepositoryDB

class RepositoryEntity(RepositoryDB[FileModel]): #, EntityCreate, EntityUpdate
    pass

entity_crud = RepositoryEntity(FileModel) 