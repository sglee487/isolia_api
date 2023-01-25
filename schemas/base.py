import re

from pydantic import BaseModel
from email_validator import validate_email as validate_e, EmailNotValidError

from database.models.enums import LoginType, BoardType


class EmailField(str):
    @classmethod
    def __get_validators__(cls):
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
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, password):
        try:
            tested = re.match("^.*(?=.{8,255})(?=.*[0-9])(?=.*[a-zA-Z]).*$", password)[
                0
            ]
            return tested
        except TypeError:
            raise ValueError("Password is not valid")


class NewPasswordField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, password):
        try:
            tested = re.match("^.*(?=.{8,255})(?=.*[0-9])(?=.*[a-zA-Z]).*$", password)[
                0
            ]
            return tested
        except TypeError:
            if password == "":
                return password
            raise ValueError("Password is not valid")


class UserBase(BaseModel):
    login_type: LoginType
    email: EmailField | None


class BoardBase(BaseModel):
    board_type: BoardType
    title: str
    content: str


class ProfilePictureBase(BaseModel):
    picture_32: str
    picture_96: str


class CommentBase(BaseModel):
    content: str
    board_id: int
