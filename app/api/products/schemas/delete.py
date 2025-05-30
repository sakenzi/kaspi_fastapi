from pydantic import BaseModel
from typing import Optional


class ProductDelete(BaseModel):
    message: str

    class Config:
        from_attributes=True