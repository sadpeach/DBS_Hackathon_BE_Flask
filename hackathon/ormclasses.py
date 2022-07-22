from sqlalchemy import Boolean, DateTime, Column, ForeignKey, Integer, String, func, Text, Float
from typing import Any

from hackathon.dbhelper import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    username = Column(String(255), nullable = False)
    password = Column(String(255), nullable = False)
    name = Column(String, nullable=False)

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name

class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.id'), nullable = False)
    name = Column(String(255), nullable = False)

    def __init__(self, user_id, name, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.user_id = user_id
        self.name = name

class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key = True)
    wallet_id = Column(Integer, ForeignKey(f'{Wallet.__tablename__}.id'), nullable=False)
    currency = Column(String(255), nullable=False)
    amount = Column(Float, nullable = False, default = 0.0)

    def __init__(self, wallet_id, currency, amount, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.wallet_id = wallet_id
        self.currency = currency
        self.amount = amount

class ExchangeRate(Base):
    __tablename__ = 'exchange_rate'
    id = Column(Integer, primary_key = True)
    base_currency = Column(String(255), nullable = False)
    exchange_currency = Column(String(255), nullable = False)
    rate = Column(Float, nullable = False)

    def __init__(self, base_currency, exchange_currency, rate, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.base_currency = base_currency
        self.exchange_currency = exchange_currency
        self.rate = rate

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key = True)
    wallet_id = Column(Integer, ForeignKey(f'{Wallet.__tablename__}.id'), nullable = False)
    debit_id = Column(Integer)
    debit_currency = Column(String(255))
    debit_amount = Column(Float, ForeignKey(f'{Currency.__tablename__}.id'), nullable = False)
    credit_id = Column(Integer)
    credit_currency = Column(String(255))
    credit_amount = Column(Float, ForeignKey(f'{Currency.__tablename__}.id'), nullable = False)
    description = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String(255)) #shouldnt this be user primary key?
    updated_at = Column(DateTime, onupdate = func.now())
    updated_by = Column(String(255))

    def __init__(self, wallet_id, \
        debit_id, debit_currency, debit_amount, \
        credit_id, credit_currency, credit_amount, \
        description, created_by, updated_by):

        self.wallet_id = wallet_id
        self.debit_id = debit_id
        self.debit_currency = debit_currency
        self.debit_amount = debit_amount
        self.credit_id = credit_id
        self.credit_currency = credit_currency
        self.credit_amount = credit_amount
        self.description = description
        self.created_by = created_by
        self.updated_by = updated_by