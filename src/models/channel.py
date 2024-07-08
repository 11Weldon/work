from sqlalchemy import String, Integer, Column, JSON, ForeignKey, ARRAY, Table, Boolean
from sqlalchemy.orm import relationship

from src.database import Base
from src.models.product import GroupProduct


class Service(Base):
    __tablename__ = 'Service'

    service_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(200))
    type = Column(String(200))
    status = Column(String(200))
    format = Column(Integer)
    mProv_id = Column(Integer)
    cProv_id = Column(Integer)
    langs = Column(Integer)


class Channel(Service):
    __tablename__ = 'Channel'

    channel_id = Column(Integer, autoincrement=True, primary_key=True)
    service_id = Column(Integer, ForeignKey('Service.service_id'), nullable=False)
    title = Column(JSON)
    descr = Column(JSON)
    custom = Column(JSON)
    image = Column(JSON)
    channel_urls = Column(JSON)

    group_product_id = Column(Integer, ForeignKey('GroupProduct.group_product_id'))
    group_product = relationship('GroupProduct', back_populates='channels')

    channel_list_id = Column(Integer, ForeignKey('ChannelList.channel_list_id'))
    channel_list = relationship("ChannelList", back_populates="channels")


class ChannelGroupProduct(Base):
    __tablename__ = 'Channel_GroupProduct'

    channel_group_product_id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey('Channel.channel_id'))
    group_product_id = Column(Integer, ForeignKey('GroupProduct.group_product_id'))

    channel = relationship("Channel", backref="channel_group_products")
    group_product = relationship("GroupProduct", backref="group_product_channels")


class ChannelList(Base):
    __tablename__ = 'ChannelList'

    channel_list_id = Column(Integer, autoincrement=True, primary_key=True)
    target_type = Column(String(200))
    target_id = Column(Integer)
    name = Column(String(200))
    type = Column(String(200))
    seqNum = Column(Integer)
    inheritable = Column(Boolean)
    locked = Column(Boolean)

    title = Column(JSON)
    descr = Column(JSON)
    entry_ids = Column(ARRAY(String))
    entry_lsns = Column(ARRAY(Integer))

    channels = relationship("Channel", back_populates="channel_list")
