import os
import smtplib

import stockquotes
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Stock

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

smtpObj = smtplib.SMTP_SSL("smtp.gmail.com", 465)

email = os.environ["EMAIL_ADDRESS"]
password = os.environ["EMAIL_PASSWORD"]

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
                + f"of ${stock.price}. It is currently at ${current_price}.\n\nLove you,\nAang"
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
                + f"of ${stock.price}. It is currently at ${current_price}.\n\nLove you,\nAang"
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
