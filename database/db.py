from boto3 import resource
from decouple import config

dynamodb = resource("dynamodb",
                    region_name=config("DB_REGION_NAME"),
                    aws_access_key_id=config("DB_AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=config("DB_AWS_SECRET_ACCESS_KEY")
                    )

tables = [
    {
        "TableName": "users",
        "AttributeDefinitions": [
            {
                'AttributeName': 'login_type',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sns_sub',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'password',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'display_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'role',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'is_active',
                'AttributeType': 'BOOL'
            },
            {
                'AttributeName': 'created_at',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'updated_at',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'deleted_at',
                'AttributeType': 'S'
            }
        ],
        "KeySchema": [
            {
                'AttributeName': 'login_type',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            },
        ],
    },
    {
        "TableName": "boards",
        "AttributeDefinitions": [
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'board_type',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'content',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'login_type',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'created_at',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'updated_at',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'deleted_at',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'is_deleted',
                'AttributeType': 'BOOL'
            },
            {
                'AttributeName': 'is_notice',
                'AttributeType': 'BOOL'
            },
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
