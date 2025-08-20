# backend-python/app/routes/product.py
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..services import product_service  # Importar el servicio

router = APIRouter()

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate, 
    db: Session = Depends(get_db)
):
    return product_service.create_product(db, product)

@router.get("/", response_model=list[schemas.Product])
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return product_service.get_products(db, skip, limit)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(
    product_id: str = Path(..., description="ID del producto"),
    db: Session = Depends(get_db)
):
    db_product = product_service.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: str,
    product_update: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    updated_product = product_service.update_product(db, product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.get("/category/{category_id}", response_model=list[schemas.Product])
def get_products_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    return product_service.get_products_by_category(db, category_id)

@router.get("/search/", response_model=list[schemas.Product])
def search_products(
    query: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return product_service.search_products(db, query, skip, limit)