import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

def upload_image(file_path: str):
    try:
        response = cloudinary.uploader.upload(file_path)
        return response['secure_url']
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None