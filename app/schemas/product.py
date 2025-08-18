from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria_id: int
    sku: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str
    
    class Config:
        orm_mode = True