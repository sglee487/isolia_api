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


async def generate_image_urls(files) -> tuple[str, str]:
    assert files

    picture_name = str(uuid.uuid4())
    # image = Image.open(file)
    #
    # picture_32, picture_96 = await asyncio.gather(
    #     upload_resized_image(image, f"{picture_name}_32", picture_name, (32, 32)),
    #     upload_resized_image(image, f"{picture_name}_96", picture_name, (96, 96)),
    # )
    # if picture_url:
    #     asyncio.create_task(remove_file(f.name))
    #
    # return picture_32, picture_96
