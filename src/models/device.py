from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Device(Base):
    __tablename__ = 'Device'

    device_id = Column(Integer, autoincrement=True, primary_key=True)
    external_id = Column(String(200))
    descr = Column(String(200))
    name = Column(JSON)