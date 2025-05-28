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


class SellerResponse(BaseModel):
    id: int

    class Config:
        from__attributes = True


class ProductsResponse(BaseModel):
    vender_code: str
    market_link: str
    name_product: str
    pieces_product: Optional[int]
    image: str
    price: int
    
    class Config:
        from__attributes = True
        

class SellerProductResponse(BaseModel):
    id: int
    seller: SellerResponse
    product: ProductsResponse

    class Config:
        from__attributes = True
