from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.auth.schemas.create import SellerRegister, SellerLogin
from model.models import Seller
from fastapi import HTTPException
from utils.context_utils import hash_password, create_access_token, verify_password
from app.api.auth.schemas.response import TokenResponse
from parsing.register_parsing import KaspiParser


async def register(seller: SellerRegister, db: AsyncSession):
    stmt = await db.execute(select(Seller).filter(Seller.kaspi_email == seller.kaspi_email))
    existing_seller = stmt.scalar_one_or_none()

    if existing_seller:
        raise HTTPException(status_code=400, detail="Такой продавец уже существует")
    
    parser = KaspiParser()
    parser.setup_driver()
    try:
        result, name_market = parser.parse_kaspi(seller.kaspi_email, seller.kaspi_password)
        if not result:
            raise HTTPException(status_code=400, detail="Неверный пароль или email")
    finally:
        parser.close_driver()
    
    hashed_password = hash_password(seller.kaspi_password)

    new_seller = Seller(
        kaspi_email=seller.kaspi_email,
        kaspi_password=hashed_password,
        name_market=name_market
    )
    db.add(new_seller)
    await db.commit()
    await db.refresh(new_seller)
    target_seller = new_seller

    access_token, expire_time = create_access_token(data={"sub": str(target_seller.id)})

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="The seller has been succesfully registered"
    )

async def login(kaspi_email: str, kaspi_password: str, db: AsyncSession):
    stmt = await db.execute(select(Seller).filter(Seller.kaspi_email == kaspi_email))

    seller = stmt.scalar_one_or_none()

    if not seller or not verify_password(kaspi_password, seller.kaspi_password):
        raise HTTPException(status_code=401, detail="Неверный пароль или пользователь")
    
    access_token, expire_time = create_access_token(data={"sub": str(seller.id)})

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time
    )
