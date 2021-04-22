from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    User model to keep track of users of the app
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    stocks = relationship("Stock", back_populates="user")


class Stock(Base):
    """
    Stock model to keep track of stocks users are watching
    """

    __tablename__ = "stocks"
    __table_args__ = (UniqueConstraint("ticker", "buy", "user_id", name="unique_stock"),)

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10))
    buy = Column(Boolean)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="stocks")
