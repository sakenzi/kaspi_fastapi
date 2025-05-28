from pydantic import BaseModel
from typing import Optional


class SellerResponse(BaseModel):
    kaspi_email: str
    kaspi_password: str

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    vender_code: str
    market_link: str

    class Config:
        from_attributes: True

class ProductComparisonResponse(BaseModel):
    min_price: int
    max_price: int
    step: int
    product: ProductResponse 

    class Config:
        from_attributes = True

class SellerProductResponse(BaseModel):
    product: ProductResponse
    seller: SellerResponse

    class Config:
        from_attributes = True