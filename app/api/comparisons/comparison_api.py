from fastapi import APIRouter, Depends
from app.api.comparisons.commands.comparison_crud import get_all_products_with_parsing
from app.api.comparisons.schemas.response import SellerProductResponse
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db


router = APIRouter()

@router.get(
    "/all-product/parsing",
    summary='Получить данные продукта для париснга',
    response_model=List[SellerProductResponse]
)
async def get_all_products(db: AsyncSession = Depends(get_db)):
    products = await get_all_products_with_parsing(db=db)
    return products