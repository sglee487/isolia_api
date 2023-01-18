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


async def upload_image_url_file(url=None, file=None, size=None, save_root_path: str = None, add_random_name: bool = False):
    assert url or file
    assert save_root_path

    if url:
        r = requests.get(url)
        filename = os.path.basename(url)
        with open(os.path.join(TEMP_FILES_FOLDER, filename), 'wb') as f:
            f.write(r.content)
            f.seek(0)
            image = Image.open(f.name)
            name, ext = os.path.splitext(filename)
    elif file:
        image = Image.open(file.file)
        name, ext = os.path.splitext(file.filename)
    else:
        raise Exception("No picture provided")

    if image.mode != 'RGB':
        image = image.convert('RGB')
    if size:
        image = image.resize(size, resample=Image.BICUBIC)
    upload_filename = f"{name}_{shortuuid.uuid()}{ext}" if add_random_name else f"{name}{ext}"
    image_path = os.path.join(TEMP_FILES_FOLDER, upload_filename)
    image.save(image_path)
    image = await s3.upload_image(image_path, f"{save_root_path}/{upload_filename}")
    asyncio.create_task(remove_file(image_path))
    return image


async def generate_image_urls(urls=None, files=None, size=None, save_root_path: str = None):
    assert urls or files
    if urls:
        urls = await asyncio.gather(
            *[asyncio.ensure_future(upload_image_url_file(url=url, size=size, save_root_path=save_root_path)) for url in urls])
    elif files:
        urls = await asyncio.gather(
            *[asyncio.ensure_future(upload_image_url_file(file=file, size=size, save_root_path=save_root_path, add_random_name=True)) for file in files])
    return urls
