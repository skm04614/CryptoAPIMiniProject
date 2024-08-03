from typing import Type
from sqlalchemy.orm import Session

from app.schema import Symbol
from app.models import SymbolRequestModel, SymbolPriceModel


def add_symbol_request(symbol: Symbol,
                       db: Session) -> SymbolRequestModel:
    symbol_request = SymbolRequestModel(
        symbol=symbol
    )
    db.add(symbol_request)
    db.commit()
    db.refresh(symbol_request)

    return symbol_request


def update_symbol_request(
    id: int,
    new_status: str,
    db: Session
) -> None:
    symbol_request = get_symbol_request(id, db)
    if not symbol_request:
        return

    symbol_request.status = new_status
    db.commit()


def get_symbol_request(
    id: int,
    db: Session
) -> Type[SymbolRequestModel] | None:
    return db.query(SymbolRequestModel).filter(SymbolRequestModel.id == id).first()


def add_symbol_price(
    symbol: Symbol,
    price: float,
    db: Session
) -> None:
    symbol_price = SymbolPriceModel(
        symbol=symbol,
        price=price
    )

    db.add(symbol_price)
    db.commit()
