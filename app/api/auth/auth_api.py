from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.auth.commands.auth_crud import register, login
from app.api.auth.schemas.response import TokenResponse
from app.api.auth.schemas.create import SellerRegister, SellerLogin
from database.db import get_db


router = APIRouter()

@router.post(
    "/seller/register",
    summary='Регистрация пользователя',

)
async def register_seller(seller: SellerRegister, db: AsyncSession = Depends(get_db)):
    return await register(seller=seller, db=db)

@router.post(
    "/seller/login",
    summary="Логин пользователя",
    response_model=TokenResponse
)
async def seller_login(login_data: SellerLogin, db: AsyncSession = Depends(get_db)):
    return await login(kaspi_email=login_data.kaspi_email, kaspi_password=login_data.kaspi_password, db=db)