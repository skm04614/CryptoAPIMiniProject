from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Symbol(str, Enum):
    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
    BNBUSDT = "BNBUSDT"
    XRPUSDT = "XRPUSDT"
    ADAUSDT = "ADAUSDT"
    SOLUSDT = "SOLUSDT"
    DOGEUSDT = "DOGEUSDT"
    DOTUSDT = "DOTUSDT"
    LTCUSDT = "LTCUSDT"
    LINKUSDT = "LINKUSDT"
    AAVEUSDT = "AAVEUSDT"
    XLMUSDT = "XLMUSDT"
    FILUSDT = "FILUSDT"
    FTTUSDT = "FTTUSDT"
    XTZUSDT = "XTZUSDT"

    @classmethod
    def list(cls):
        return [e.value for e in Symbol]


class SymbolPriceSchema(BaseModel):
    symbol: Symbol
    timestamp: datetime
    price: float

    model_config = ConfigDict(from_attributes=True)


class SymbolPriceWithIDSchema(SymbolPriceSchema):
    id: int

    def __lt__(self, other):
        if not isinstance(other, SymbolPriceSchema):
            raise NotImplementedError

        return -self.price < -other.price  # max heap에서의 사용 목적
