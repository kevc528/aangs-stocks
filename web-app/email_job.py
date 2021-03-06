import os
import smtplib

import stockquotes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Stock

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@postgres:5432"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

smtpObj = smtplib.SMTP_SSL("smtp.gmail.com", 465)

email = os.getenv("EMAIL_ADDRESS", "your-email-address")
password = os.getenv("EMAIL_PASSWORD", "your-email-password")

smtpObj.login(email, password)

for ticker in db.query(Stock.ticker).distinct():
    symbol = ticker[0]
    current_price = stockquotes.Stock(symbol).current_price

    symbol_stocks = db.query(Stock).filter(Stock.ticker == symbol)

    for stock in symbol_stocks:
        if stock.mode == "buy" and stock.price > current_price:
            subject = f"Buy {stock.ticker} Now!"
            text = (
                f"Hello,\n\nThe price for {stock.ticker} is now below your requested price"
                + f" of ${stock.price:.2f}. It is currently at ${current_price:.2f}.\n\n"
                + "Love you,\nAang"
            )
            message = "Subject: {}\n\n{}".format(subject, text)

            try:
                smtpObj.sendmail(email, stock.user.email, message)
            except smtplib.SMTPException:
                print("Email failed")
            db.delete(stock)
        elif stock.mode == "sell" and stock.price < current_price:
            subject = f"Sell {stock.ticker} Now!"
            text = (
                f"Hello,\n\nThe price for {stock.ticker} is now above your requested price"
                + f" of ${stock.price:.2f}. It is currently at ${current_price:.2f}.\n\n"
                + "Love you,\nAang"
            )
            message = "Subject: {}\n\n{}".format(subject, text)

            try:
                smtpObj.sendmail(email, stock.user.email, message)
            except smtplib.SMTPException:
                print("Email failed")
            db.delete(stock)
        else:
            stock.current_price = current_price
        db.commit()
