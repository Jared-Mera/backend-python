from sqlalchemy import Column, Integer, String, Text
from .base import Base

class Category(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    
    def __repr__(self):
        return f"<Category(id={self.id}, nombre='{self.nombre}')>"
