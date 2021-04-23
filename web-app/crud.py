import bcrypt
import stockquotes
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
    stock.ticker = stock.ticker.upper()
    stock_obj = stockquotes.Stock(stock.ticker)
    current_price = stock_obj.current_price
    print(stock_obj, current_price)
    user_id = get_user_by_email(db, email).id
    db_stock = Stock(**stock.dict(), user_id=user_id, current_price=current_price)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def delete_stock_for_user(db: Session, stock_id, email: str):
    user_id = get_user_by_email(db, email).id
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if stock.user_id == user_id:
        db.delete(stock)
        db.commit()
    else:
        raise PermissionError()
