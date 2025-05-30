from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from app.api.products.schemas.resposnse import ProductResponse, SellerProductResponse
from app.api.products.commands.product_crud import (parse_product_data, get_all_products_with_comparisons, update_is_active, 
                                                    delete_product, update_product_comparison)
from database.db import get_db
from utils.context_utils import validate_access_token, get_access_token
from app.api.products.schemas.create import AddProductCreate
from typing import List
import logging
from app.api.products.schemas.update import ProductUpdate, ProductComparisonUpdate
from app.api.products.schemas.delete import ProductDelete


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/add-product",
    summary="Добавить товар для мониторинга",
    response_model=ProductResponse
)
async def parse_product(request: Request, body: AddProductCreate, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    seller_id_str = await validate_access_token(access_token)

    try:
        seller_id = int(seller_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Недопустимый формат идентификатора пользователя в токене")
    
    data = await parse_product_data(db=db, seller_id=seller_id, vender_code=body.vender_code, min_price=body.min_price, max_price=body.max_price, step=body.step)
    return {"product": data}


@router.get(
    "/all-products",
    summary="Получить все товары пользователя с данными сравнений",
    response_model=List[SellerProductResponse]
)
async def get_products(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    seller_id_str = await validate_access_token(access_token)
    
    if not seller_id_str or not isinstance(seller_id_str, str):
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    try:
        seller_id = int(seller_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid seller_id: must be a valid integer")
    
    seller_products = await get_all_products_with_comparisons(seller_id=seller_id, db=db)
    logger.debug(f"Returning seller_products: {seller_products}")
    return seller_products

@router.put(
    "/update/is_active",
    summary="Обновить is_active продукта"
)
async def update_product(request: Request, product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    seller_id_str = await validate_access_token(access_token)

    if not seller_id_str or not isinstance(seller_id_str, str):
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    try:
        seller_id = int(seller_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid seller_id: must be a valid integer")
    
    product_is_active = await update_is_active(db=db, seller_id=seller_id, product_id=product_id, is_active=product.is_active)
    return product_is_active

@router.delete(
    "/delete",
    summary="Удалить продукт",
    response_model=ProductDelete
)
async def delete(request: Request, product_id: int, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    seller_id_str = await validate_access_token(access_token)

    if not seller_id_str or not isinstance(seller_id_str, str):
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    try:
        seller_id = int(seller_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid seller_id: must be a valid integer")
    
    product_delete = await delete_product(db=db, seller_id=seller_id, product_id=product_id)
    return product_delete

@router.put(
    "/update/digital-data",
    summary="Обновить цифровые данные продукта",
    response_model=ProductComparisonUpdate
)
async def update_digital_data(request: Request, product_id: int, product: ProductComparisonUpdate, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    seller_id_str = await validate_access_token(access_token)

    if not seller_id_str or not isinstance(seller_id_str, str):
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    try:
        seller_id = int(seller_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid seller_id: must be a valid integer")
    
    product_digital_data = await update_product_comparison(
        db=db, 
        seller_id=seller_id, 
        product_id=product_id, 
        min_price=product.min_price,
        max_price=product.max_price,
        step=product.step
    )
    return product_digital_data