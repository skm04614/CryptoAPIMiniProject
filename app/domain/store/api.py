from multiprocessing import Process
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema import Symbol
from app.domain.store import crud
from app.domain.store.task import query_binance

router = APIRouter(
    prefix="/store",
    tags=["store"]
)


@router.get("")
def get_symbols():
    return {"symbol": Symbol.list()}


@router.post("/{symbol}")
def add_symbol_request(
    symbol: Symbol,
    db: Session = Depends(get_db)
):
    symbol_request = crud.add_symbol_request(symbol, db)

    Process(target=query_binance,
            args=(symbol_request.id, symbol),
            daemon=True).start()

    return {"id": symbol_request.id}


@router.get("/store/result/{id}")
def get_symbol_request_status(
    id: int,
    db: Session = Depends(get_db)
):
    symbol_request = crud.get_symbol_request(id, db)
    if not symbol_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id={id} does not exist.")

    return {"status": symbol_request.status}
