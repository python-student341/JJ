from pydantic import Field, BaseModel, EmailStr
from enum import Enum


class Status(str, Enum):
    viewed = 'viewed'
    shortlisted = 'shortlisted'
    interview = 'interview'
    rejected = 'rejected'
    hired = 'hired'

class ResponseSchema(BaseModel):
    cover_letter: str = Field(min_length=0, max_length=100, pattern=r'^[a-zA-Zа-яА-Я0-9\s\.,!\?\-\(\):;]+$')

class ApplicantReadSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

class ResumeReadSchema(BaseModel):
    id: int
    title: str
    stack: str

class ResponseReadSchema(BaseModel):
    id: int
    cover_letter: str
    resume: ResumeReadSchema
    user: ApplicantReadSchema

class SetStatusSchema(BaseModel):
    status: Status