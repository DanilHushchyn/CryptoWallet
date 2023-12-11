import re
from typing import Optional

from pydantic import (
    BaseModel, EmailStr,
)
from email_validator import validate_email, EmailNotValidError


# Profile schemas
class UserModel(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserProfile(BaseModel):
    username: str = ''
    new_password: str = ''
    repeat_password: str = ''
    avatar: str = ''


class UserForm(BaseModel):
    id: int
    email: EmailStr
    username: str
    avatar: str


# Profile schemas
class AuthUsers(BaseModel):
    email: EmailStr
    password: str
    remember: bool = False


class RegisterUserModel(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str
