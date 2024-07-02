from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    hash_init = Column(String(200), nullable=False)

    household = relationship('Household', back_populates='user')


class Household(Base):
    __tablename__ = 'Household'

    household_id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(Integer, nullable=False)
    description = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False)
    accnt_code = Column(String(50), nullable=False)
    locale_id = Column(Integer, nullable=False)
    max_devices = Column(Integer, nullable=False)
    max_users = Column(Integer, nullable=False)
    max_profiles = Column(Integer, nullable=False)
    no_pers = Column(Boolean, nullable=False)
    custom = Column(JSON)  # JSON column to store custom attributes

    user_id = Column(Integer, ForeignKey('User.user_id'))
    user = relationship('User', back_populates='household')