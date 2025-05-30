from pydantic import BaseModel
from typing import Optional


class ProductUpdate(BaseModel):
    price: Optional[int] = None
    pieces_product: Optional[int] = None

    class Config:
        from_attributes=True