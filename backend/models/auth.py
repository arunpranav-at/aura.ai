from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    avatar: str
    password: str


class SignInRequest(BaseModel):
    username: str
    password: str
