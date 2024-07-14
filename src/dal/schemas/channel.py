from sqlalchemy import String, Integer, JSON, ForeignKey, ARRAY, Boolean, Table, Column
from sqlalchemy.orm import mapped_column, relationship

from src.dal.schemas import Base


class ServiceORM(Base):
    __tablename__ = 'Service'
    __table_args__ = {"schema": "clients_schema"}

    service_id = mapped_column(String, primary_key=True)
    name = mapped_column(String)
    type = mapped_column(String)
    status = mapped_column(String)
    format = mapped_column(Integer)
    mProv_id = mapped_column(Integer)
    cProv_id = mapped_column(Integer)
    langs = mapped_column(Integer)


class ChannelORM(Base):
    __tablename__ = 'Channel'
    __table_args__ = {"schema": "clients_schema"}

    channel_id = mapped_column(Integer, primary_key=True)
    service_id = mapped_column(String, ForeignKey('clients_schema.Service.service_id'), nullable=False)
    name = mapped_column(String)
    type = mapped_column(String)
    status = mapped_column(String)
    title = mapped_column(JSON)
    format = mapped_column(Integer)
    mProv_id = mapped_column(Integer)
    cProv_id = mapped_column(Integer)
    langs = mapped_column(Integer)
    description = mapped_column(JSON)
    custom = mapped_column(JSON)
    image = mapped_column(JSON)
    channel_urls = mapped_column(JSON)




class ChannelListORM(Base):
    __tablename__ = 'ChannelList'
    __table_args__ = {"schema": "clients_schema"}

    channel_list_id = mapped_column(Integer, primary_key=True)
    target_type = mapped_column(String)
    target_id = mapped_column(Integer)
    name = mapped_column(String)
    type = mapped_column(String)
    seqNum = mapped_column(Integer)
    inheritable = mapped_column(Boolean)
    locked = mapped_column(Boolean)

    title = mapped_column(JSON)
    description = mapped_column(JSON)
    entry_ids = mapped_column(ARRAY(String))
    entry_lsns = mapped_column(ARRAY(Integer))
