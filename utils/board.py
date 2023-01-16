import os
import uuid
import random
import requests
import asyncio

from PIL import Image
from services.s3 import S3Service
import shortuuid

from utils.util import remove_file
from constants import TEMP_FILES_FOLDER

s3 = S3Service()


async def upload_image_file(file, user_id):
    image = Image.open(file.file)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    name, ext = os.path.splitext(file.filename)
    upload_filename = f"{name}_{shortuuid.uuid()}{ext}"
    image_path = os.path.join(TEMP_FILES_FOLDER, upload_filename)
    image.save(image_path)
    image = await s3.upload_image(image_path, f"board/{user_id}/{upload_filename}")
    asyncio.create_task(remove_file(image_path))
    return image


async def generate_image_urls(files, user_id=None):
    urls = await asyncio.gather(*[asyncio.ensure_future(upload_image_file(file, user_id)) for file in files])
    return urls
