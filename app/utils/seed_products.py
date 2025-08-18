# backend-python/app/utils/seed_products.py
import random
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Product, Category
from faker import Faker
from ..utils.cloudinary import upload_image  # Añadir
import tempfile
import requests
import os
import time

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
    
    # Lista de imágenes de prueba (URLs públicas)
    # Reemplazar con URLs funcionales de Picsum
    sample_images = [
        "https://picsum.photos/id/1/200/300",
        "https://picsum.photos/id/10/200/300",
        "https://picsum.photos/id/100/200/300",
        "https://picsum.photos/id/1000/200/300",
        "https://picsum.photos/id/1001/200/300",
        "https://picsum.photos/id/1002/200/300",
        "https://picsum.photos/id/1003/200/300",
        "https://picsum.photos/id/1004/200/300",
        "https://picsum.photos/id/1005/200/300",
        "https://picsum.photos/id/1006/200/300",
    ]

    # Generar 200 productos de prueba
    for i in range(1, 201):
        # Seleccionar una categoría aleatoria
        category = random.choice(categories)
        
        # Generar datos ficticios para el producto
        product_name = f"Producto {i} - {fake.word().capitalize()}"
        sku_prefix = ''.join([c[0] for c in category.nombre.split()]).upper()
        
        random_image_url = random.choice(sample_images)
        imagen_url = None

        max_retries = 3

        for attempt in range(max_retries):
            try:
                # Descargar imagen con timeout
                response = requests.get(random_image_url, timeout=10)
                response.raise_for_status()
                
                if response.content:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
                        temp.write(response.content)
                        temp_path = temp.name
                    
                    if os.path.getsize(temp_path) > 0:
                        imagen_url = upload_image(temp_path)
                    else:
                        print(f"⚠️ Archivo vacío: {random_image_url}")
                    os.unlink(temp_path)
                    break  # Salir del bucle si tiene éxito
                else:
                    print(f"⚠️ Contenido vacío en: {random_image_url}")
                    
            except Exception as e:
                print(f"❌ Error en intento {attempt+1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    # Espera exponencial: 1s, 2s, 4s
                    sleep_time = 2 ** attempt
                    print(f"⏳ Esperando {sleep_time}s antes de reintentar...")
                    time.sleep(sleep_time)
                else:
                    print(f"❌ Fallo definitivo con la imagen: {random_image_url}")
        
        # Pequeña pausa entre productos para no saturar
        time.sleep(0.1)

        # Crear producto
        new_product = Product(
            nombre=product_name,
            descripcion=fake.sentence(),
            precio=round(random.uniform(10.0, 1000.0), 2),
            stock=random.randint(0, 100),
            categoria_id=category.id,
            sku=f"{sku_prefix}-{fake.unique.bothify(text='####-####')}",
            imagen_url=imagen_url
        )
        
        db.add(new_product)
        
        # Mostrar progreso cada 50 productos
        if i % 10 == 0:
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