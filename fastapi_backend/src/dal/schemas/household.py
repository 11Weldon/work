from sqlalchemy import Integer, String, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from src.database import Base


class UserProfileORM(Base):
    __tablename__ = 'user_profile'
    __table_args__ = {"schema": "clients_schema"}

    user_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255))
    password = mapped_column(String(255))
    first_name = mapped_column(String(100))
    last_name = mapped_column(String(100))
    status = mapped_column(String(50))
    address = mapped_column(String(255))
    phone = mapped_column(String(20))
    hash_init = mapped_column(String(255))

    households = relationship("Household", back_populates="user_profile")


class HouseholdORM(Base):
    __tablename__ = 'household'
    __table_args__ = {"schema": "clients_schema"}

    household_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain = mapped_column(Integer)
    description = mapped_column(String(255))
    status = mapped_column(String(50))
    accnt_code = mapped_column(String(50))
    locale_id = mapped_column(Integer)
    max_devices = mapped_column(Integer)
    max_users = mapped_column(Integer)
    max_profiles = mapped_column(Integer)
    no_pers = mapped_column(Boolean)
    custom = mapped_column(JSON)

    user_profile_id = mapped_column(Integer, ForeignKey('clients_schema.user_profile.user_id'))
    user_profile = relationship("UserProfile", back_populates="households")

    profiles = relationship("Profile", secondary="household_profile", backref="households")
    products = relationship("Products", secondary="household_product", backref="households")


class ProfileORM(Base):
    __tablename__ = 'profile'
    __table_args__ = {"schema": "clients_schema"}

    profile_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(200))
    type = mapped_column(String(200))
    description= mapped_column(String(200))
    age = mapped_column(Integer)
    pin = mapped_column(Integer)
    purchasePin = mapped_column(Integer)
    custom = mapped_column(JSON)
    image = mapped_column(JSON)


class HouseholdProfileORM(Base):
    __tablename__ = 'household_profile'
    __table_args__ = {"schema": "clients_schema"}

    household_profile_id = mapped_column(Integer, primary_key=True)
    profile_id = mapped_column(Integer, ForeignKey('clients_schema.profile.profile_id'))
    household_id = mapped_column(Integer, ForeignKey('clients_schema.household.household_id'))

    profile = relationship("Profile", backref="household_profiles")
    household = relationship("Household", backref="household_profiles")


class HouseholdProductORM(Base):
    __tablename__ = 'household_product'
    __table_args__ = {"schema": "clients_schema"}

    household_product_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    household_id = mapped_column(Integer, ForeignKey('clients_schema.household.household_id'))
    product_id = mapped_column(Integer, ForeignKey('clients_schema.Products.product_id'))

    household = relationship("Household", backref="household_products")
    product = relationship("Products", backref="product_households")
