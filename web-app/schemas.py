from pydantic import BaseModel


class UserBase(BaseModel):
    """
    User base schema for common attributes from both read and write
    """

    email: str


class UserPassword(UserBase):
    """
    Additional field needed when writing
    """

    password: str


class User(UserBase):
    """
    Additional field returned when reading
    """

    id: int

    class Config:
        orm_mode = True
