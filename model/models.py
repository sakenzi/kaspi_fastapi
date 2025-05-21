from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
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
    vender_code = Column(Integer, nullable=False)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    step = Column(Float, nullable=True)
    product_link = Column(Text, nullable=True)

    seller_products = relationship("SellerProduct", back_populates="product")

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    vender_code_pay = Column(Integer, nullable=False)
    vender_code_market = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)

class SellerProduct(Base):
    __tablename__ = "seller_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)

    product = relationship("Product", back_populates="seller_products")
    seller = relationship("Seller", back_populates="seller_products")