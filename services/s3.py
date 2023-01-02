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

    def upload_file(self, file, object_name=None):
        if object_name is None:
            object_name = file.filename
        try:
            self.s3.upload_fileobj(
                file,
                self.bucket,
                object_name,
                ExtraArgs={"ACL": "public-read"},
            )
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{object_name}"
        except Exception as e:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "S3 service is not available")

    def delete_file(self, bucket_name, object_name):
        self.s3.delete_object(
            Bucket=bucket_name,
            Key=object_name,
        )