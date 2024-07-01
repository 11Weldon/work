from typing import Annotated

from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


class Client(Base):
    __tablename__ = 'Client'

    client_id: Mapped[intpk]
    client_name: Mapped[str]
    client_balance: Mapped[int] = mapped_column(nullable=False)


class ClientBundle(Base):
    __tablename__ = 'ClientBundle'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('Client.client_id'))
    bundle_id = Column(Integer, ForeignKey('Bundle.bundle_id'))

    client = relationship('Client', backref='client_bundles')
    bundle = relationship('Bundle', backref='client_bundles')

    @classmethod
    def link_client_to_bundle(cls, session, client_id, bundle_id):
        client_bundle = cls(client_id=client_id, bundle_id=bundle_id)
        session.add(client_bundle)
        return client_bundle


class Bundle(Base):
    __tablename__ = 'Bundle'

    bundle_id = Column(Integer, primary_key=True)
    bundle_title = Column(String(200), nullable=False)

    channels = relationship('Channel', secondary='BundleChannel', backref='bundles')


class Channel(Base):
    __tablename__ = 'Channel'

    channel_id = Column(Integer, primary_key=True)
    channel_title = Column(String(200), nullable=False)
    bundle_id = Column(Integer, ForeignKey('Bundle.bundle_id'))

    bundle = relationship('Bundle', back_populates='channels')


class BundleChannel(Base):
    __tablename__ = 'BundleChannel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bundle_id = Column(Integer, ForeignKey('Bundle.bundle_id'))
    channel_id = Column(Integer, ForeignKey('Channel.channel_id'))

    bundle = relationship('Bundle', backref='bundle_channels')
    channel = relationship('Channel', backref='bundle_channels')
