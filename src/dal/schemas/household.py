from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, JSON
from sqlalchemy.orm import mapped_column, relationship

from src.dal.schemas import Base
from src.dal.schemas.bundle import bundle_household_association


class HouseholdORM(Base):
    __tablename__ = 'household'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain_id = mapped_column(Integer, nullable=True)
    contact = mapped_column(Integer, nullable=True)
    description = mapped_column(String, nullable=True)
    created = mapped_column(DateTime, default=datetime.utcnow)
    status = mapped_column(Integer, nullable=True)
    account_code = mapped_column(String, unique=True, nullable=False)
    locale_id = mapped_column(Integer, nullable=True)
    max_devices = mapped_column(Integer, nullable=True)
    max_users = mapped_column(Integer, nullable=True)
    max_profiles = mapped_column(Integer, nullable=True)
    no_personalization = mapped_column(Boolean, nullable=True)
    time_stamp = mapped_column(DateTime, default=datetime.utcnow)

    bundles = relationship('BundleORM', secondary=bundle_household_association, back_populates='households')
    # acc_code = mapped_column(String, primary_key=True)
    # first_name = mapped_column(String)
    # last_name = mapped_column(String)
    # address = mapped_column(String)
    # phone = mapped_column(String)
    # domain_id = mapped_column(Integer)
    # is_enabled = mapped_column(Boolean)
    # no_pers = mapped_column(Boolean)
    # master_PIN = mapped_column(String(4))
    # username = mapped_column(String)
    # hashed_pwd = mapped_column(Boolean)
    # password = mapped_column(String)
    # hash_init = mapped_column(String, nullable=True)

    # upsell_info = relationship('UpsellInfo', back_populates='household')

    products = relationship("HouseholdToProductORM", back_populates="household")


class UserORM(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=True)
    type = mapped_column(Integer, nullable=True)
    password = mapped_column(String, nullable=True)
    first_name = mapped_column(String, nullable=True)
    last_name = mapped_column(String, nullable=True)
    status = mapped_column(Integer, nullable=True)
    address = mapped_column(String, nullable=True)
    phone = mapped_column(String, nullable=True)
    household_id = mapped_column(Integer, nullable=True)
    default_profile_id = mapped_column(Integer, nullable=True)
    default_profile = mapped_column(String, nullable=True)
    time_stamp = mapped_column(DateTime, default=datetime.utcnow)


class ClientProfileORM(Base):
    __tablename__ = 'client_profile'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    household_id = mapped_column(Integer, nullable=True)
    description = mapped_column(String, nullable=True)
    age = mapped_column(Integer, nullable=True)
    pin = mapped_column(String, nullable=True)
    purchase_pin = mapped_column(String, nullable=True)
    custom_data = mapped_column(String, nullable=True)
    type_id = mapped_column(Integer, nullable=True)
    name = mapped_column(String, unique=True, nullable=True)
    image_urls = mapped_column(JSON, nullable=True)
    time_stamp = mapped_column(DateTime, default=datetime.utcnow)


class UserProfilesORM(Base):
    __tablename__ = 'user_profiles'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer)
    profile_id = mapped_column(Integer, nullable=True)

