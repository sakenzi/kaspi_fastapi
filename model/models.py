from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean, Text, func
from sqlalchemy.orm import relationship
from database.db import Base


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name_market = Column(String(250), nullable=True)
    kaspi_email = Column(String(250), nullable=True, unique=True)
    kaspi_password = Column(Text, nullable=True)

    seller_products = relationship("SellerProduct", back_populates="seller")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    vender_code = Column(String(200), nullable=False)
    market_link = Column(Text, nullable=False)
    name_product = Column(Text, nullable=False)
    pieces_product = Column(Integer, nullable=True)
    image = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=False)
    first_market = Column(String(250), nullable=False)
    price_first_market = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    seller_products = relationship("SellerProduct", back_populates="product")
    product_comparisons = relationship("ProductComparison", back_populates="product")

class ProductComparison(Base):
    __tablename__ = "product_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    min_price = Column(Integer, nullable=True)
    max_price = Column(Integer, nullable=True)
    step = Column(Integer, nullable=True)

    product_id = Column(Integer, ForeignKey("products.id", ondelete='CASCADE'), nullable=False)

    product = relationship("Product", back_populates="product_comparisons")

class SellerProduct(Base):
    __tablename__ = "seller_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete='CASCADE'), nullable=False, )
    seller_id = Column(Integer, ForeignKey("sellers.id", ondelete='CASCADE'), nullable=False)

    product = relationship("Product", back_populates="seller_products")
    seller = relationship("Seller", back_populates="seller_products")