import os

import boto3
from decouple import config
from fastapi import HTTPException

from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


class S3Service:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket = config("AWS_BUCKET_NAME")
        self.region = config("AWS_REGION")

    async def upload_image(self, path, key):
        _, ext = os.path.splitext(key)
        ext = ext[1:]
        try:
            self.s3.upload_file(
                path,
                self.bucket,
                key,
                ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"},
            )
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        except ValueError as e:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, e)
        except Exception as e:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "S3 service is not available")

    def delete_file(self, bucket_name, object_name):
        self.s3.delete_object(
            Bucket=bucket_name,
            Key=object_name,
        )