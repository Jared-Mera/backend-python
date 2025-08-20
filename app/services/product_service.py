# backend-python/app/services/product_service.py
from sqlalchemy.orm import Session
from .. import models
from ..schemas import ProductCreate, Product
from ..database import get_db
from typing import List
import uuid
from sqlalchemy import or_

def create_product(db: Session, product: ProductCreate) -> models.Product:
    """
    Crea un nuevo producto en la base de datos
    """
    # Generar UUID para el producto
    product_id = str(uuid.uuid4())
    
    db_product = models.Product(
        id=product_id,
        nombre=product.nombre,
        descripcion=product.descripcion,
        precio=product.precio,
        stock=product.stock,
        categoria_id=product.categoria_id,
        sku=product.sku,
        imagen_url=product.imagen_url
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
#Obtener producto por ID

def get_product(db: Session, product_id: str) -> models.Product:
    """
    Obtiene un producto por su ID 
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """
    Obtiene una lista de productos con paginación
    """
    return db.query(models.Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: str, product_update: ProductCreate) -> models.Product:
    """
    Actualiza un producto existente
    """
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if db_product:
        for key, value in product_update.dict().items():
            setattr(db_product, key, value)
        
        db.commit()
        db.refresh(db_product)
    
    return db_product
#Eliminar productos

def delete_product(db: Session, product_id: str) -> bool:
    """
    Elimina un producto por su ID
    """
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
#Obtiene Productos
def get_products_by_category(db: Session, category_id: int) -> List[models.Product]:
    """
    Obtiene productos por categoría
    """
    return db.query(models.Product).filter(models.Product.categoria_id == category_id).all()

#Buscar productos o producto

def search_products(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """
    Busca productos por nombre o descripción
    """
    return db.query(models.Product).filter(
        or_(
            models.Product.nombre.ilike(f"%{query}%"),
            models.Product.descripcion.ilike(f"%{query}%"),
            models.Product.sku.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()
