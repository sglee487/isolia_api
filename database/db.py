from boto3 import resource
from decouple import config

dynamodb = resource("dynamodb",
                    region_name=config("DB_REGION_NAME"),
                    aws_access_key_id=config("DB_AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=config("DB_AWS_SECRET_ACCESS_KEY")
                    )

tables = [
    {
        "TableName": config("DB_USER_TABLE_NAME"),
        "AttributeDefinitions": [
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'login_type',
                'AttributeType': 'S'
            }
        ],
        "KeySchema": [
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'login_type',
                'KeyType': 'RANGE'
            }
        ],
    },
    {
        "TableName": config("DB_BOARD_TABLE_NAME"),
        "AttributeDefinitions": [
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        "KeySchema": [
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
    },
]


def create_tables():
    try:
        for table in tables:
            dynamodb.create_table(
                TableName=table["TableName"],
                KeySchema=table["KeySchema"],
                AttributeDefinitions=table["AttributeDefinitions"],
                BillingMode="PAY_PER_REQUEST"
            )
    except Exception as e:
        print(e)
