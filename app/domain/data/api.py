from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schema import Symbol, SymbolPriceSchema
from app.domain.data import crud

router = APIRouter(
    prefix="/data",
    tags=["data"]
)


@router.get("")
def get_symbol_prices(
    page: int = 1,
    db: Session = Depends(get_db)
):
    return crud.get_symbol_prices(page, db)


@router.get("/{symbol}")
def get_specific_symbol_prices(
    symbol: Symbol,
    db: Session = Depends(get_db)
):
    return crud.get_specific_symbol_prices(symbol, db)


@router.get("/{symbol}/max")
def get_specific_symbol_max_price(
    symbol: Symbol,
    db: Session = Depends(get_db)
):
    return crud.get_specific_symbol_max_price(symbol, db)


@router.get("/{symbol}/wmax/{window}", response_model=list[SymbolPriceSchema])
def get_specific_symbol_moving_max_prices(
    symbol: Symbol,
    window: int,
    db: Session = Depends(get_db)
):
    return crud.get_specific_symbol_moving_max_prices(symbol, window, db)
