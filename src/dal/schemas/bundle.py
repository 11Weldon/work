from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, Table, Column, JSON, Boolean, DateTime
from sqlalchemy.orm import mapped_column, relationship

from src.dal.schemas import Base

# bundle_upsell_association = Table(
#     'bundle_upsell_association',
#     Base.metadata,
#     Column('bundle_id', Integer, ForeignKey('bundle.id')),
#     Column('transaction_id', String, ForeignKey('upsell_info.transaction_id'))
# )

product_bundle_association = Table(
    'product_bundle_association',
    Base.metadata,
    Column('bundle_id', Integer, ForeignKey('bundle.id')),
    Column('product_id', Integer, ForeignKey('product.id'))
)

bundle_household_association = Table(
    'bundle_household_association',
    Base.metadata,
    Column('bundle_id', Integer, ForeignKey('bundle.id')),
    Column('household_id', Integer, ForeignKey('household.id'))
)


class BundleORM(Base):
    __tablename__ = 'bundle'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id = mapped_column(String, unique=True, nullable=False)
    name = mapped_column(String, nullable=True)
    title = mapped_column(JSON, nullable=True)
    description = mapped_column(JSON, nullable=True)
    is_add_on = mapped_column(Boolean, nullable=True)
    custom_data = mapped_column(JSON, nullable=True)
    image_urls = mapped_column(JSON, nullable=True)
    time_stamp = mapped_column(DateTime, default=datetime.utcnow)

    # upsell_info_list = relationship("UpsellInfo",
    #                                 secondary=bundle_upsell_association,
    #                                 back_populates="bundle_list")

    products = relationship("ProductORM",
                            secondary=product_bundle_association,
                            back_populates="bundles")

    households = relationship('HouseholdORM', secondary=bundle_household_association, back_populates='bundles')

# class UpsellInfo(Base):
#     __tablename__ = 'upsell_info'
#
#     transaction_id = mapped_column(String, primary_key=True)
#     acc_code = mapped_column(String, ForeignKey('household.account_code'))
#     trigger_type = mapped_column(String)
#     trigger_id = mapped_column(String)
#
#     household = relationship('HouseholdORM', back_populates='upsell_info')
#
#     bundle_list = relationship("BundleORM",
#                                secondary=bundle_upsell_association,
#                                back_populates="upsell_info_list")
