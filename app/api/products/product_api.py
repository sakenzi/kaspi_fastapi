from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from app.api.products.schemas.resposnse import ProductResponse, SellerProductResponse, ProductsResponse, SellerResponse
from app.api.products.commands.product_crud import parse_product_data, get_all_products
from database.db import get_db
from utils.context_utils import validate_access_token, get_access_token
from app.api.products.schemas.create import AddProductCreate
from typing import List


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
    summary="Получить все товары пользователя",
    response_model=List[SellerProductResponse]
)
async def get_products(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    seller_id_str = await validate_access_token(access_token)
    
    if not seller_id_str or not isinstance(seller_id_str, str):
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    try:
        seller_id = int(seller_id_str)  # Convert string to int
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid seller_id: must be a valid integer")
    
    return await get_all_products(seller_id=seller_id, db=db)