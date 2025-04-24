from fastapi import APIRouter, UploadFile
import shutil

from src.services.images import ImageService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
def upload_image(file: UploadFile):
    ImageService().upload_image(file)
