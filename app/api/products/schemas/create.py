from pydantic import BaseModel
from typing import Optional


class ProductComparisonCreate(BaseModel):
    article_number: int
    market_link: int
    name_product: str
    image: str
    price: int
    min_price: int
    max_price: int
    step: int

