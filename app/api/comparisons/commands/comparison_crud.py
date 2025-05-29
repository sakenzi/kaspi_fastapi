from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from model.models import SellerProduct, Product
from typing import List
from sqlalchemy.orm import selectinload, joinedload


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