import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import category, product
from .routes import product as product_routes, category as category_routes
from .database import get_db

app = FastAPI(
    title="Productos API",
    description="API para gestión de productos y categorías",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Crear tablas si no existen
    category.Base.metadata.create_all(bind=engine)
    product.Base.metadata.create_all(bind=engine)

    # Crear categorías iniciales
    db = next(get_db())
    try:
        await category_routes.create_initial_categories(db)
    finally:
        db.close()

# Incluir rutas
app.include_router(product_routes.router, prefix="/api/products", tags=["products"])
app.include_router(category_routes.router, prefix="/api/categories", tags=["categories"])

@app.get("/")
def root():
    return {
        "message": "API de Productos en funcionamiento",
        "version": app.version,
        "docs": "/docs"
    }