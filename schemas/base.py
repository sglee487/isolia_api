import re

from pydantic import BaseModel
from email_validator import validate_email as validate_e, EmailNotValidError


class EmailField(str):
    @classmethod
    def __get_validator__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, email):
        try:
            validate_e(email)
            return email
        except EmailNotValidError:
            raise ValueError("Email is not valid")


class PasswordField(str):
    @classmethod
    def __get_validator__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, password):
        try:
            tested = re.match('^.*(?=.{8,255})(?=.*[0-9])(?=.*[a-zA-Z]).*$', password)[0]
            return tested
        except TypeError:
            raise ValueError("Password is not valid")


class UserBase(BaseModel):
    email: EmailField
