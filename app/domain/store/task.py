import ccxt
from time import sleep

from app.schema import Symbol
from app.domain.store.crud import update_symbol_request, add_symbol_price
from app.database import get_context_managed_db


def query_binance(
    id: int,
    symbol: Symbol
) -> None:
    success = False
    try:
        for _ in range(10):
            binance = ccxt.binance()

            with get_context_managed_db() as db:
                add_symbol_price(symbol, binance.fetch_ticker("BTCUSDT")["last"], db)
            sleep(1)
    except Exception:
        pass
    else:
        success = True
    finally:
        with get_context_managed_db() as db:
            update_symbol_request(id,
                                  "OK" if success else "FAIL",
                                  db)
