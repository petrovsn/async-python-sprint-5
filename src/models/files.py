from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base

from .base import Base





class File(Base):
    # Имя таблицы в базе данных
    __tablename__ = "File"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String, default = None)
    size = Column(Integer)
    path = Column(String)
    is_downloadable = Column(Boolean)

    # Значение `eager_defaults` указывает ORM немедленно получать значение
    # сгенерированных сервером значений по умолчанию для INSERT или UPDATE.
    __mapper_args__ = {"eager_defaults": True}

    
    # Чтобы сделать консольный вывод более информативным, добавим __repr__
    def __repr__(self):
        return f"File: {self.path}"