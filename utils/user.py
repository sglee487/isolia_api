import os
import uuid
import random
import requests
import asyncio

from PIL import Image
from services.s3 import S3Service

from utils.util import remove_file
from constants import TEMP_FILES_FOLDER

s3 = S3Service()


def generate_random_name() -> str:
    adj_list = []
    with open("utils/korean_adj.txt", "r", encoding="UTF8") as f:
        lines = f.readlines()
        for line in lines:
            adj_list.append(line.strip())

    noun_list = []
    with open("utils/korean_noun.txt", "r", encoding="UTF8") as f:
        lines = f.readlines()
        for line in lines:
            noun_list.append(line.strip())

    return f"{random.choice(adj_list)} {random.choice(noun_list)} {random.randrange(1, 100)}"


async def upload_resized_image(image, name, key, size):
    image = image.resize(size, resample=Image.BICUBIC)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image_path = os.path.join(TEMP_FILES_FOLDER, f"{name}.jpg")
    image.save(image_path)
    image = await s3.upload_image(image_path, f"profile_images/{size[0]}/{key}.jpg")
    asyncio.create_task(remove_file(image_path))
    return image


async def generate_profile_urls(picture_url=None, file=None) -> tuple[str, str]:
    assert picture_url or file

    picture_name = str(uuid.uuid4())
    if picture_url:
        r = requests.get(picture_url)
        with open(os.path.join(TEMP_FILES_FOLDER, picture_name), 'wb') as f:
            f.write(r.content)
            f.seek(0)
            image = Image.open(f.name)
    elif file:
        image = Image.open(file)
    else:
        raise Exception("No picture provided")

    picture_32, picture_96 = await asyncio.gather(
        upload_resized_image(image, f"{picture_name}_32", picture_name, (32, 32)),
        upload_resized_image(image, f"{picture_name}_96", picture_name, (96, 96)),
    )
    if picture_url:
        asyncio.create_task(remove_file(f.name))

    return picture_32, picture_96
