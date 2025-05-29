from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


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

    class Config:
        from_attributes = True


class SellerResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True

class ProductComparisonResponse(BaseModel):
    id: int
    min_price: Optional[int]
    max_price: Optional[int]
    step: Optional[int]

    class Config:
        from_attributes = True

class ProductsResponse(BaseModel):
    vender_code: str
    market_link: str
    name_product: str
    pieces_product: Optional[int]
    image: str
    price: int
    is_active: bool
    updated_at: datetime
    comparisons: Optional[List[ProductComparisonResponse]] = Field(default=None, alias="product_comparisons")

    class Config:
        from_attributes = True

class SellerProductResponse(BaseModel):
    id: int
    seller: SellerResponse
    product: ProductsResponse

    class Config:
        from_attributes = True