from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from backend.src.database import Base

class DeviceTypes(Base):
    __tablename__ = 'DeviceTypes'

    device_types_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(JSON)
    device_category_id = Column(Integer, ForeignKey('DeviceCategories.device_categories_id'))

    device_categories = relationship("DeviceCategories", back_populates="device_type")


class DeviceCategories(Base):
    __tablename__ = 'DeviceCategories'

    device_categories_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(JSON)

    devices = relationship("Device", back_populates="device_category")
    device_type = relationship("DeviceTypes", back_populates="device_categories")


class Device(Base):
    __tablename__ = 'Device'

    device_id = Column(Integer, autoincrement=True, primary_key=True)
    external_id = Column(String(200))
    descr = Column(String(200))
    name = Column(JSON)
    device_category_id = Column(Integer, ForeignKey('DeviceCategories.device_categories_id'))

    device_category = relationship("DeviceCategories", back_populates="devices")
