from pydantic import BaseModel
from typing import Optional


class ProductUpdate(BaseModel):
    is_active: Optional[bool] = None

    class Config:
        from_attributes=True


class ProductComparisonUpdate(BaseModel):
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    step: Optional[int] = None

    class Config:
        from_attributes=True