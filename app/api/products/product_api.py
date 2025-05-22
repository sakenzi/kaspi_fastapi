from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from app.api.products.schemas.resposnse import ProductResponse
from app.api.products.commands.product_crud import parse_product_data
from database.db import get_db
from utils.context_utils import validate_access_token, get_access_token


router = APIRouter()

@router.post(
    "/add-product",
    summary="Добавить товар для мониторинга",
    response_model=ProductResponse
)
async def parse_product(request: Request, vender_code: str, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    seller_id_str = await validate_access_token(access_token)

    try:
        seller_id = int(seller_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Недопустимый формат идентификатора пользователя в токене")
    
    data = await parse_product_data(db, seller_id, vender_code)
    return {"product": data}