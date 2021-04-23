from typing import List

from pydantic import BaseModel


class StockBase(BaseModel):
    ticker: str
    mode: str
    price: float


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    id: int
    current_price: float

    class Config:
        orm_mode = True


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

    stocks: List[Stock] = []

    class Config:
        orm_mode = True
