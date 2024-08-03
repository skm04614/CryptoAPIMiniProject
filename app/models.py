from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
import pytz

from app.database import Base


def kr_time():
    return datetime.now(pytz.timezone("Asia/Seoul"))


class SymbolRequestModel(Base):
    __tablename__ = "symbol_request"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    status = Column(String,
                    nullable=False,
                    default="PROCESSING")


class SymbolPriceModel(Base):
    __tablename__ = "symbol_price"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    timestamp = Column(DateTime,
                       nullable=False,
                       default=kr_time)
    price = Column(Float, nullable=False)
