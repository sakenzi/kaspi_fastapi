from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from model.models import SellerProduct, Product
from typing import List
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


async def get_all_products_with_parsing(db: AsyncSession) -> List[SellerProduct]:
    query = (
        select(SellerProduct)
        .options(
            selectinload(SellerProduct.product).selectinload(Product.product_comparisons),
            joinedload(SellerProduct.seller)
        )
    )
    result = await db.execute(query)
    products = result.scalars().all()

    return products

async def update_product_parsing(product_id: int, product_data: dict, db: AsyncSession):
    query = (
        select(Product).filter(Product.id == product_id)
    )
    result = await db.execute(query)
    product_parsing = result.scalars().first()

    for key, value in product_data.items():
        if value is not None:
            setattr(product_parsing, key, value)

    try:
        await db.commit()
        await db.refresh(product_parsing)
        return product_parsing
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="")