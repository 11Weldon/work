from typing import Annotated

from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, str_256
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


class Client(Base):
    __tablename__ = 'Client'

    client_id: Mapped[intpk]
    client_name: Mapped[str]
    client_balance: Mapped[int] = mapped_column(nullable=False)


class ClientTariff(Base):
    __tablename__ = 'ClientTariff'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('Client.client_id'))
    tariff_id = Column(Integer, ForeignKey('Tariff.tariff_id'))

    client = relationship('Client', backref='client_tariffs')
    tariff = relationship('Tariff', backref='client_tariffs')

    @classmethod
    def link_client_to_tariff(cls, session, client_id, tariff_id):
        client_tariff = cls(client_id=client_id, tariff_id=tariff_id)
        session.add(client_tariff)
        return client_tariff


class Tariff(Base):
    __tablename__ = 'Tariff'

    tariff_id = Column(Integer, primary_key=True)
    tariff_title = Column(String(200), nullable=False)

    functions = relationship('Function', secondary='TariffFunction', backref='tariffs')


class Function(Base):
    __tablename__ = 'Function'

    function_id = Column(Integer, primary_key=True)
    function_title = Column(String(200), nullable=False)
    tariff_id = Column(Integer, ForeignKey('Tariff.tariff_id'))

    tariff = relationship('Tariff', back_populates='functions')


class TariffFunction(Base):
    __tablename__ = 'TariffFunction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tariff_id = Column(Integer, ForeignKey('Tariff.tariff_id'))
    function_id = Column(Integer, ForeignKey('Function.function_id'))

    tariff = relationship('Tariff', backref='tariff_functions')
    function = relationship('Function', backref='tariff_functions')

    @classmethod
    def link_tariff_to_function(cls, session, tariff_id, function_id):
        tariff_function = cls(tariff_id=tariff_id, function_id=function_id)
        session.add(tariff_function)
        return tariff_function
