from pydantic import BaseModel


class RegisterUserDto(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str


class LoginDto(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str


class UserDto(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str