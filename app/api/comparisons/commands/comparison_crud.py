from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from model.models import ProductComparison, Seller, SellerProduct, Product


async def get_all_products(db: AsyncSession):
    query = (select())