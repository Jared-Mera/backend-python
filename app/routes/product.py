# backend-python/app/routes/product.py
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..services import product_service  # Importar el servicio
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from sqlalchemy import func


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

# GET /api/products/summary
@router.get("/summary")
def get_products_summary(db: Session = Depends(get_db)):
    total_products = db.query(func.count(models.Product.id)).scalar()
    low_stock = db.query(models.Product).filter(models.Product.stock < 10).count()
    
    return {
        "total": total_products,
        "lowStock": low_stock
    }

# GET /api/products/top-selling
@router.get("/top-selling")
def get_top_selling_products(db: Session = Depends(get_db)):
    # Esto sería más eficiente si tienes una tabla de ventas en PostgreSQL
    # En este ejemplo asumimos que tienes una tabla de ventas
    top_products = db.query(
        models.Product.nombre,
        func.sum(models.SaleItem.quantity).label('total_quantity')
    ).join(
        models.SaleItem, models.SaleItem.product_id == models.Product.id
    ).group_by(
        models.Product.id
    ).order_by(
        func.sum(models.SaleItem.quantity).desc()
    ).limit(10).all()
    
    return [
        {"name": p[0], "quantity": p[1]} 
        for p in top_products
    ]