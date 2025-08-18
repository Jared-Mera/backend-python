# backend-python/app/routes/category.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Category, CategoryCreate
from ..services import category_service

router = APIRouter()

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, category)

@router.get("/", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    return category_service.get_categories(db)

@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return category

@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int, 
    category_update: CategoryCreate, 
    db: Session = Depends(get_db)
):
    return category_service.update_category(db, category_id, category_update)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if not category_service.delete_category(db, category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return

# Función para crear categorías iniciales
async def create_initial_categories(db: Session = Depends(get_db)):
    initial_categories = [
        {"nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos de consumo"},
        {"nombre": "Ropa", "descripcion": "Prendas de vestir"},
        {"nombre": "Alimentos", "descripcion": "Productos alimenticios"},
        {"nombre": "Hogar", "descripcion": "Artículos para el hogar"},
        {"nombre": "Deportes", "descripcion": "Artículos deportivos"}
    ]
    
    for category_data in initial_categories:
        if not category_service.get_category_by_name(db, category_data["nombre"]):
            category_service.create_category(db, CategoryCreate(**category_data))
    
    print("✅ Categorías iniciales creadas")