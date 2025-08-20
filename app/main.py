import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import category, product
from .routes import product as product_routes, category as category_routes
from .database import get_db
from .routes import upload

app = FastAPI(
    title="Productos API",
    description="API para gestión de productos y categorías",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "*",
        "https://res.cloudinary.com"
    ],
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
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])

@app.get("/")
def root():
    return {
        "message": "API de Productos en funcionamiento",
        "version": app.version,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), reload=True)
