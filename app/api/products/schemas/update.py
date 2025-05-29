from pydantic import BaseModel
from typing import Optional


class ProductUpdate(BaseModel):
    is_active: Optional[bool] = None

    class Config:
        from_attributes=True