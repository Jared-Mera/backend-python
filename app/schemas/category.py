from pydantic import BaseModel

class CategoryBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True