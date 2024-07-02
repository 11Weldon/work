from typing import Annotated

from sqlalchemy import String, Integer, Column, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


class Client(Base):
    __tablename__ = 'Client'

    client_id: Mapped[intpk]
    client_name: Mapped[str]
    client_balance: Mapped[int] = mapped_column(nullable=False)


class ClientProduct(Base):
    __tablename__ = 'ClientProduct'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('Client.client_id'))
    product_id = Column(Integer, ForeignKey('Product.product_id'))

    client = relationship('Client', backref='client_products')
    product = relationship('Product', backref='client_products')


class Product(Base):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True)
    product_title = Column(String(200), nullable=False)

    channels = relationship('Channel', secondary='ProductChannel', backref='products')


class Channel(Base):
    __tablename__ = 'Channel'

    channel_id = Column(Integer, autoincrement=True, primary_key=True)
    channel_title = Column(String(200), nullable=False)
    synopsis_short = Column(JSON)
    synopsis_long = Column(JSON)
    keywords = Column(JSON)
    audio = Column(JSON)
    live_url = Column(String(255))
    time_stamp = Column(String(50))
    service_id = Column(Integer)
    transport_id = Column(Integer)
    rec_adapter_id = Column(Integer)

    product_id = Column(Integer, ForeignKey('Product.product_id'))
    product = relationship('Product', back_populates='channels')


class ProductChannel(Base):
    __tablename__ = 'ProductChannel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Product.product_id'))
    channel_id = Column(Integer, ForeignKey('Channel.channel_id'))

    product = relationship('Product', backref='product_channels')
    channel = relationship('Channel', backref='product_channels')


class Domain(Base):
    __tablename__ = 'Domain'

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain_title = Column(JSON)
    domain_descr = Column(JSON)


class ChannelMapping(Base):
    __tablename__ = 'channel_mapping'

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer)
    target_id = Column(Integer)
    type = Column(String)
    mapped = Column(String)
