from datetime import datetime

from sqlalchemy import String, DateTime, Integer, JSON, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, relationship

from src.dal.schemas import Base
from src.dal.schemas.bundle import product_bundle_association


class ProductORM(Base):
    __tablename__ = 'product'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id = mapped_column(String, unique=True, nullable=False)
    type = mapped_column(Integer, nullable=True)
    valid_start = mapped_column(DateTime, nullable=True)
    valid_end = mapped_column(DateTime, nullable=True)
    status = mapped_column(Integer, nullable=True)

    image_urls = mapped_column(JSON, nullable=True)
    time_stamp = mapped_column(DateTime, default=datetime.utcnow)
    name = mapped_column(String, nullable=True)
    title = mapped_column(JSON, nullable=True)
    description = mapped_column(JSON, nullable=True)
    feat_prod_id = mapped_column(Integer, nullable=True)
    custom_data = mapped_column(JSON, nullable=True)

    households = relationship("HouseholdToProductORM", back_populates="product")
    prices = mapped_column(JSON, nullable=True)
    bundles = relationship("BundleORM",
                           secondary=product_bundle_association,
                           back_populates="products")


class HouseholdToProductORM(Base):
    __tablename__ = 'household_to_product'

    household_to_product_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    household_id = mapped_column(Integer, ForeignKey("household.id"))
    product_id = mapped_column(Integer, ForeignKey("product.id"))

    is_enabled = mapped_column(Boolean, default=False)

    product = relationship("ProductORM", back_populates="households")
    household = relationship("HouseholdORM", back_populates="products")
