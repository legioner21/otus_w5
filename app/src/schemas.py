from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    avatar: str
    age: int


class UserProfileBase(BaseModel):
    avatar: str
    age: int


class UserProfileDto(UserProfileBase):
    id: int

    class Config:
        orm_mode = True
