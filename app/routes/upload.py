from fastapi import APIRouter, UploadFile, File
from ..utils.cloudinary import upload_image
import tempfile
import os

router = APIRouter()

@router.post("/upload")
async def upload_image_endpoint(file: UploadFile = File(...)):
    try:
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name
        
        # Subir a Cloudinary
        image_url = upload_image(temp_path)
        os.unlink(temp_path)  # Eliminar temporal
        
        if image_url:
            return {"image_url": image_url}
        return {"error": "Failed to upload image"}, 500
    except Exception as e:
        return {"error": str(e)}, 500
