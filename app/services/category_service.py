# backend-python/app/services/category_service.py
from sqlalchemy.orm import Session
from .. import models
from ..schemas import CategoryCreate, Category
from ..database import get_db
from typing import List, Optional
from fastapi import HTTPException, status

def create_category(db: Session, category: CategoryCreate) -> models.Category:
    """
    Crea una nueva categoría en la base de datos
    
    Args:
        db: Sesión de base de datos
        category: Datos de la categoría a crear
    
    Returns:
        La categoría creada
    """
    # Verificar si la categoría ya existe
    existing_category = db.query(models.Category).filter(
        models.Category.nombre.ilike(category.nombre)
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría '{category.nombre}' ya existe"
        )
    
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Obtiene una categoría por su ID
    
    Args:
        db: Sesión de base de datos
        category_id: ID de la categoría
    
    Returns:
        La categoría si existe, None si no
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """
    Obtiene todas las categorías con paginación
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar
        limit: Número máximo de registros a devolver
    
    Returns:
        Lista de categorías
    """
    return db.query(models.Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category_update: CategoryCreate) -> models.Category:
    """
    Actualiza una categoría existente
    
    Args:
        db: Sesión de base de datos
        category_id: ID de la categoría a actualizar
        category_update: Datos actualizados
    
    Returns:
        La categoría actualizada
    """
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Verificar si el nuevo nombre ya existe
    if category_update.nombre != db_category.nombre:
        existing_category = db.query(models.Category).filter(
            models.Category.nombre.ilike(category_update.nombre),
            models.Category.id != category_id
        ).first()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La categoría '{category_update.nombre}' ya existe"
            )
    
    # Actualizar campos
    for key, value in category_update.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    """
    Elimina una categoría por su ID
    
    Args:
        db: Sesión de base de datos
        category_id: ID de la categoría a eliminar
    
    Returns:
        True si se eliminó, False si no
    
    Raises:
        HTTPException: Si la categoría tiene productos asociados
    """
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not db_category:
        return False
    
    # Verificar si la categoría tiene productos asociados
    product_count = db.query(models.Product).filter(
        models.Product.categoria_id == category_id
    ).count()
    
    if product_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una categoría con productos asociados"
        )
    
    db.delete(db_category)
    db.commit()
    return True

def get_category_by_name(db: Session, name: str) -> Optional[models.Category]:
    """
    Obtiene una categoría por su nombre
    
    Args:
        db: Sesión de base de datos
        name: Nombre de la categoría
    
    Returns:
        La categoría si existe, None si no
    """
    return db.query(models.Category).filter(
        models.Category.nombre.ilike(name)
    ).first()