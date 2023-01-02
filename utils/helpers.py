import base64

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


def decode_photo(path, encoded_string):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_string.encode('utf-8')))
        except Exception as e:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid photo encoding")
