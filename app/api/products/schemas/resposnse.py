from pydantic import BaseModel
from typing import Optional


class OneProductResponse(BaseModel):
    vender_code: str
    name_product: str
    price: int
    pieces_product: int
    image: str
    market_link: str
    seller_product_id: int

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    product: OneProductResponse
