from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Coin:
    id: str
    symbol: str
    name: str
    current_price: float
    market_cap: float
    total_volume: float
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    ath: Optional[float] = None
    atl: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    ohlc: Optional[List] = field(default=None)
    sparkline: Optional[str] = field(default=None)

    @classmethod
    def from_api(cls, data: dict):
        """Create Coin object from CoinGecko dict, ignoring unknown keys"""
        allowed_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered_data)