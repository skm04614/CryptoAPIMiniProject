import heapq
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schema import Symbol, SymbolPriceSchema, SymbolPriceWithIDSchema
from app.models import SymbolPriceModel

_page_size = 10


def get_symbol_prices(
    page: int,
    db: Session
) -> list[SymbolPriceSchema]:
    result = (
        db.query(SymbolPriceModel)
        .order_by(SymbolPriceModel.id.desc())
        .offset((page - 1) * _page_size)
        .limit(_page_size)
        .all()
    )

    return [SymbolPriceSchema.from_orm(res) for res in result]


def get_specific_symbol_prices(
    symbol: Symbol,
    db: Session
) -> list[SymbolPriceSchema]:
    result = (
        db.query(SymbolPriceModel)
        .filter(SymbolPriceModel.symbol == symbol)
        .order_by(SymbolPriceModel.id.desc())
        .limit(_page_size)
        .all()
    )

    return [SymbolPriceSchema.from_orm(res) for res in result]


def get_specific_symbol_max_price(
    symbol: Symbol,
    db: Session
) -> SymbolPriceSchema | None:
    subquery = (
        db.query(SymbolPriceModel)
        .filter(SymbolPriceModel.symbol == symbol)
        .order_by(SymbolPriceModel.id.desc())
        .limit(_page_size)
        .subquery()
    )

    result = (
        db.query(SymbolPriceModel)
        .select_from(subquery)
        .order_by(subquery.c.price.desc())
        .first()
    )

    if result is None:
        return None

    return SymbolPriceSchema.from_orm(result)


def get_specific_symbol_moving_max_prices(
    symbol: Symbol,
    window: int,
    db: Session
) -> list[SymbolPriceWithIDSchema]:
    pool = (
        db.query(SymbolPriceModel)
        .filter(SymbolPriceModel.symbol == symbol)
        .order_by(SymbolPriceModel.id.desc())
        .limit(window + _page_size - 1)
        .all()
    )

    if len(pool) < window + _page_size - 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is not enough data to handle the"
                                   "requested window size.")

    pool = [SymbolPriceWithIDSchema.from_orm(entry) for entry in pool]
    max_heap: list[SymbolPriceWithIDSchema] = []
    for entry in pool[:window - 1]:
        heapq.heappush(max_heap, entry)

    result: list[SymbolPriceWithIDSchema] = []
    for entry in pool[window:]:
        while entry.id >= entry.id + window:
            heapq.heappop(max_heap)

        heapq.heappush(max_heap, entry)
        result.append(max_heap[0])

    return result
