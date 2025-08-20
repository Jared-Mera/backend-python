from sqlalchemy import Column, String, Text, Numeric, Integer, ForeignKey
from .base import Base
import uuid

class Product(Base):
    __tablename__ = 'productos'

    id = Column(String(50), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    sku = Column(String(50), unique=True)
    imagen_url = Column(String(255))  # Linea para la nueva columna para URL de imagen
    
    def __repr__(self):
        return f"<Product(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"