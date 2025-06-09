from pydantic import BaseModel
from typing import Optional


class ProductComparisonCreate(BaseModel):
    article_number: int
    market_link: int
    first_market: str
    price_first_market: int
    name_product: str
    image: str
    price: int
    min_price: int
    max_price: int
    step: int

class AddProductCreate(BaseModel):
    vender_code: str
    min_price: int
    max_price: int
    step: int