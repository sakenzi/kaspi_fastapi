from fastapi import APIRouter, Depends
from app.api.comparisons.commands.comparison_crud import get_all_products_with_parsing, update_product_parsing
from app.api.comparisons.schemas.response import SellerProductResponse
from app.api.comparisons.schemas.update import ProductUpdate
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

@router.put(
    "/update/",
    summary="Обновление данных во время парсинга",
    response_model=ProductUpdate
)
async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product_data = product.dict(exclude_unset=True)
    updated_product = await update_product_parsing(product_id, product_data, db)

    return updated_product