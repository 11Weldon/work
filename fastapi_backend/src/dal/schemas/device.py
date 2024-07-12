from sqlalchemy import Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from src.database import Base


class DeviceTypesORM(Base):
    __tablename__ = 'DeviceTypes'
    __table_args__ = {"schema": "clients_schema"}

    device_types_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(JSON)
    device_category_id = mapped_column(Integer, ForeignKey('clients_schema.DeviceCategories.device_categories_id'))

    device_categories = relationship("DeviceCategories", back_populates="device_type")


class DeviceCategoriesORM(Base):
    __tablename__ = 'DeviceCategories'
    __table_args__ = {"schema": "clients_schema"}

    device_categories_id = mapped_column(Integer, autoincrement=True, primary_key=True)
    name = mapped_column(JSON)

    devices = relationship("Device", back_populates="device_category")
    device_type = relationship("DeviceTypes", back_populates="device_categories")


class DeviceORM(Base):
    __tablename__ = 'Device'
    __table_args__ = {"schema": "clients_schema"}

    device_id = mapped_column(Integer, autoincrement=True, primary_key=True)
    external_id = mapped_column(String(200))
    description = mapped_column(String(200))
    name = mapped_column(JSON)
    device_category_id = mapped_column(Integer, ForeignKey('clients_schema.DeviceCategories.device_categories_id'))

    device_category = relationship("DeviceCategories", back_populates="devices")
