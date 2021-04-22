import bcrypt
from sqlalchemy.orm import Session

from models import Stock, User
from schemas import StockCreate, UserPassword


# create a new user in the database
def create_user(db: Session, user: UserPassword):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(email=user.email, hashed_password=hashed_password.decode("utf-8"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def add_stock_for_user(db: Session, stock: StockCreate, email: str):
    user_id = get_user_by_email(db, email).id
    db_stock = Stock(**stock.dict(), user_id=user_id)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock
