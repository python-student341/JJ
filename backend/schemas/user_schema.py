from pydantic import Field, BaseModel, EmailStr
from enum import Enum


class Role(str, Enum):
    tenant = 'tenant'
    applicant = 'applicant'


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')
    repeat_password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')
    role: Role
    name: str = Field(min_length=3, max_length=15, pattern=r'^[a-zA-Zа-яА-Я\s]+$')

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')

class EditUserPasswordSchema(BaseModel):
    old_password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')
    new_password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')
    repeat_new_password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')

class EditUserNameSchema(BaseModel):
    new_name: str = Field(min_length=3, max_length=15, pattern=r'^[a-zA-Zа-яА-Я\s]+$')
    password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')

class DeleteUserSchema(BaseModel):
    password: str = Field(min_length=8, max_length=25, pattern=r'^[a-zA-Z0-9@#$%^&+=]+$')