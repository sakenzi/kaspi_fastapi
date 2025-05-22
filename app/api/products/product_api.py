from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from app.api.products.schemas.resposnse import ProductResponse
from app.api.products.commands.product_crud import parse_product_data
from database.db import get_db
from utils.context_utils import validate_access_token, get_access_token
from app.api.products.schemas.create import AddProductCreate


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