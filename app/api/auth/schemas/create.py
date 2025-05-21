from pydantic import BaseModel, Field
from typing import Optional


class SellerRegister(BaseModel):
    kaspi_email: Optional[str] = Field("", max_length=250)
    kaspi_password: str = Field(..., min_length=6)

class SellerLogin(BaseModel):
    kaspi_email: str = Field(..., max_length=250)
    kaspi_password: str = Field(..., min_length=6)