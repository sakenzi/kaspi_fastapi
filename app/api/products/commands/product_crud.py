from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.api.products.schemas.create import ProductComparisonCreate
from parsing.add_product_parsing import KaspiParser
from model.models import Seller, Product, SellerProduct, ProductComparison
from utils.config_utils import decrypt_password
from app.api.products.schemas.resposnse import ProductResponse
from typing import List
from sqlalchemy.orm import joinedload


async def parse_product_data(db: AsyncSession, seller_id: int, vender_code: str, min_price: int, max_price: int, step: int) -> ProductResponse:
    query = await db.execute(select(Seller).where(Seller.id == seller_id))
    seller = query.scalar_one_or_none()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    kaspi_email = seller.kaspi_email
    kaspi_password = decrypt_password(seller.kaspi_password)

    parser = KaspiParser()
    parser.setup_driver()
    try:
        result = parser.parse_kaspi(vender_code, kaspi_email, kaspi_password)
    finally:
        parser.close_driver()

    if not result:
        raise HTTPException(status_code=400, detail="Такого артикула нет или неправильно")

    stmt = select(Product).where(Product.vender_code == vender_code)
    res = await db.execute(stmt)
    product = res.scalars().first()

    if not product:
        product = Product(
            vender_code=vender_code,
            name_product=result["name_product"],
            price=result["price"],
            pieces_product=result["pieces_product"],
            image=result["image"],
            market_link=result["market_link"]
        )
        db.add(product)
        await db.commit()
        await db.refresh(product)

    stmt = select(SellerProduct).where(
        SellerProduct.seller_id == seller_id,
        SellerProduct.product_id == product.id
    )
    res = await db.execute(stmt)
    seller_product = res.scalars().first()

    if not seller_product:
        seller_product = SellerProduct(
            seller_id=seller_id,
            product_id=product.id
        )
        db.add(seller_product)
        await db.commit()
        await db.refresh(seller_product)

    comparison = ProductComparison(
        min_price=min_price,
        max_price=max_price,
        step=step,
        product_id=product.id
    )
    db.add(comparison)
    await db.commit()

    return {
        "vender_code": product.vender_code,
        "name_product": product.name_product,
        "price": product.price,
        "pieces_product": product.pieces_product,
        "image": product.image,
        "market_link": product.market_link,
        "seller_product_id": seller_product.id,
    }


async def get_all_products(seller_id: int, db: AsyncSession) -> List[SellerProduct]:
    query = (
        select(SellerProduct)
        .where(SellerProduct.seller_id == seller_id)
        .options(
            joinedload(SellerProduct.product),
            joinedload(SellerProduct.seller)
        )
    )
    result = await db.execute(query)
    seller_products = result.scalars().all()
    
    if not seller_products:
        raise HTTPException(status_code=404, detail="No products found for this seller")
    
    return seller_products
