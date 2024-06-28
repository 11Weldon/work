from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    __tablename__ = 'Client'

    client_id = Column(Integer, primary_key=True)
    client_name = Column(String(200))
    client_balance = Column(Integer, nullable=False)


class Service(Base):
    __tablename__ = 'Service'

    service_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('Client.client_id'))
    tariff_id = Column(Integer, ForeignKey('Tariff.tariff_id'))

    client = relationship('Client', back_populates='services')
    tariff = relationship('Tariff', back_populates='services')


class Tariff(Base):
    __tablename__ = 'Tariff'

    tariff_id = Column(Integer, primary_key=True)
    tariff_title = Column(String(200), nullable=False)

    functions = relationship('Function', back_populates='tariff')


class Function(Base):
    __tablename__ = 'Function'

    function_id = Column(Integer, primary_key=True)
    function_title = Column(String(200), nullable=False)
    tariff_id = Column(Integer, ForeignKey('Tariff.tariff_id'))

    tariff = relationship('Tariff', back_populates='functions')




