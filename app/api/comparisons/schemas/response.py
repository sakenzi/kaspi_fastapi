from pydantic import BaseModel, Field
from typing import Optional, List


class SellerResponse(BaseModel):
    kaspi_email: str
    kaspi_password: str

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
    market_link: str
    vender_code: str
    comparisons: Optional[List[ProductComparisonResponse]] = Field(default=None, alias="product_comparisons")

    class Config:
        from_attributes = True


class SellerProductResponse(BaseModel):
    id: int
    seller: SellerResponse
    product: ProductsResponse

    class Config:
        from_attributes = True