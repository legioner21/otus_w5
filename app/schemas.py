from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str
    phone: str


class CreateUserDto(UserBase):
    pass


class UpdateUserDto(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str


class UserDto(UserBase):
    id: int

    class Config:
        orm_mode = True