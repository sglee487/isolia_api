from boto3 import resource
from decouple import config

dynamodb = resource("dynamodb",
                    region_name=config("AWS_REGION_NAME"),
                    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY")
                    )

# database = databases.Database(DATABASE_URL)
# metadata = sqlalchemy.MetaData()
