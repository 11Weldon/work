from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.database import Base
from src.models.channel import Product


class UserProfile(Base):
    __tablename__ = 'user_profile'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    password = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    status = Column(String(50))
    address = Column(String(255))
    phone = Column(String(20))
    hash_init = Column(String(255))

    households = relationship("Household", back_populates="user_profile")


class Household(Base):
    __tablename__ = 'household'

    household_id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(Integer)
    description = Column(String(255))
    status = Column(String(50))
    accnt_code = Column(String(50))
    locale_id = Column(Integer)
    max_devices = Column(Integer)
    max_users = Column(Integer)
    max_profiles = Column(Integer)
    no_pers = Column(Boolean)
    custom = Column(JSON)

    user_profile_id = Column(Integer, ForeignKey('user_profile.user_id'), nullable=False)
    user_profile = relationship("UserProfile", back_populates="households")

    profiles = relationship("Profile", secondary="household_profile", backref="households")
    products = relationship("Product", secondary="household_product", backref="households")


class Profile(Base):
    __tablename__ = 'profile'

    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    type = Column(String(200))
    descr = Column(String(200))
    age = Column(Integer)
    pin = Column(Integer)
    purchasePin = Column(Integer)
    custom = Column(JSON)
    image = Column(JSON)


class HouseholdProfile(Base):
    __tablename__ = 'household_profile'

    household_profile_id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profile.profile_id'))
    household_id = Column(Integer, ForeignKey('household.household_id'))

    profile = relationship("Profile", backref="household_profiles")
    household = relationship("Household", backref="household_profiles")


class HouseholdProduct(Base):
    __tablename__ = 'household_product'

    household_product_id = Column(Integer, primary_key=True, autoincrement=True)
    household_id = Column(Integer, ForeignKey('household.household_id'))
    product_id = Column(Integer, ForeignKey('Product.product_id'))

    household = relationship("Household", backref="household_products")
    product = relationship("Product", backref="product_households")
