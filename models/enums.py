import enum


class RoleType(enum.Enum):
    admin = "admin"
    user = "user"


class LoginType(enum.Enum):
    email = "email"
    naver = "naver"
    google = "google"
    apple = "apple"
