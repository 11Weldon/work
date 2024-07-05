from sqlalchemy import String, Integer, Column, JSON, ForeignKey, ARRAY, Table
from sqlalchemy.orm import relationship

from src.database import Base


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

    product_id = Column(Integer, ForeignKey('Product.product_id'))
    product = relationship('Product', back_populates='channels')


class Product(Base):
    __tablename__ = 'Product'

    product_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(JSON)

    channels = relationship('Channel', secondary='Channel_Product', backref='products')


class ChannelProduct(Base):
    __tablename__ = 'Channel_Product'

    phannel_product_id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey('Channel.channel_id'))
    product_id = Column(Integer, ForeignKey('Product.product_id'))

    channel = relationship("Channel", backref="channel_products")
    product = relationship("Product", backref="product_channels")
