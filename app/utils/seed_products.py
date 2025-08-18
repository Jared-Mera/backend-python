# backend-python/app/utils/seed_products.py
import random
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Product, Category
from faker import Faker

def seed_products():
    """
    Genera y carga categorías y 200 productos de prueba en la base de datos
    """
    fake = Faker()
    db = SessionLocal()
    
    # Crear categorías predeterminadas si no existen
    default_categories = [
        {"nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos de consumo"},
        {"nombre": "Ropa", "descripcion": "Prendas de vestir para hombres, mujeres y niños"},
        {"nombre": "Alimentos", "descripcion": "Productos alimenticios y bebidas"},
        {"nombre": "Hogar", "descripcion": "Artículos para el hogar y decoración"},
        {"nombre": "Deportes", "descripcion": "Equipamiento deportivo y actividades al aire libre"}
    ]
    
    created_categories = []
    for cat_data in default_categories:
        existing_category = db.query(Category).filter_by(nombre=cat_data["nombre"]).first()
        if not existing_category:
            new_category = Category(**cat_data)
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
            created_categories.append(new_category)
            print(f"✅ Categoría creada: {new_category.nombre}")
    
    # Obtener todas las categorías existentes
    categories = db.query(Category).all()
    
    if not categories:
        print("❌ No hay categorías disponibles después de intentar crearlas.")
        db.close()
        return
    
    # Generar 200 productos de prueba
    for i in range(1, 201):
        # Seleccionar una categoría aleatoria
        category = random.choice(categories)
        
        # Generar datos ficticios para el producto
        product_name = f"Producto {i} - {fake.word().capitalize()}"
        sku_prefix = ''.join([c[0] for c in category.nombre.split()]).upper()
        
        # Crear producto con datos ficticios
        new_product = Product(
            nombre=product_name,
            descripcion=fake.sentence(),
            precio=round(random.uniform(10.0, 1000.0), 2),
            stock=random.randint(0, 100),
            categoria_id=category.id,
            sku=f"{sku_prefix}-{fake.unique.bothify(text='####-####')}"
        )
        
        db.add(new_product)
        
        # Mostrar progreso cada 50 productos
        if i % 50 == 0:
            print(f"🔄 Generados {i} productos...")
    
    try:
        db.commit()
        print("✅ 200 productos creados exitosamente")
        print(f"📊 Distribución por categorías:")
        for cat in categories:
            count = db.query(Product).filter_by(categoria_id=cat.id).count()
            print(f"   - {cat.nombre}: {count} productos")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear productos: {e}")
    finally:
        db.close()

# Ejecutar el script solo si se llama directamente
if __name__ == "__main__":
    seed_products()