from pydantic import Field, BaseModel

from backend.schemas.user_schema import Role

class EditUserNameByAdmin(BaseModel):
    new_name: str = Field(min_length=3, max_length=15, pattern=r'^[a-zA-Zа-яА-Я\s]+$')

class UpdateUserRole(BaseModel):
    new_role: Role