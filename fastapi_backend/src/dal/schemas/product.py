from sqlalchemy import Integer, JSON, ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column
from src.database import Base


class GroupToProductsORM(Base):
    __tablename__ = 'GroupToProducts'
    __table_args__ = {"schema": "clients_schema"}

    group_to_products_id = mapped_column(Integer, primary_key=True)
    group_product_id = mapped_column(Integer, ForeignKey('clients_schema.GroupProduct.group_product_id'))
    product_id = mapped_column(Integer, ForeignKey('clients_schema.Products.product_id'))

    group_product = relationship("GroupProductORM", backref="group_to_products")
    product = relationship("ProductsORM", backref="group_associations")


class GroupProductORM(Base):
    __tablename__ = 'GroupProduct'
    __table_args__ = {"schema": "clients_schema"}

    group_product_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id = mapped_column(String(200))
    type = mapped_column(String(200))
    status = mapped_column(String(200))
    name = mapped_column(String(200))
    title = mapped_column(JSON)
    description= mapped_column(JSON)
    custom = mapped_column(JSON)
    prices = mapped_column(JSON)
    image = mapped_column(JSON)

    products = relationship("ProductsORM", secondary="GroupToProductsORM", backref="groups")

    channels = relationship('ChannelORM', secondary='Channel_GroupProduct', backref='products')


class FeatureProductORM(Base):
    __tablename__ = 'FeatureProduct'
    __table_args__ = {"schema": "clients_schema"}

    feature_product_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id = mapped_column(String(200))
    status = mapped_column(String(200))
    name = mapped_column(String(200))
    quota = mapped_column(Integer)
    valid_period = mapped_column(Integer)
    title = mapped_column(JSON)
    description= mapped_column(JSON)
    custom = mapped_column(JSON)
    prices = mapped_column(JSON)
    image = mapped_column(JSON)

    products = relationship("ProductsORM", secondary="FeatureToProducts", backref="features")


class ProductsORM(Base):
    __tablename__ = 'Products'
    __table_args__ = {"schema": "clients_schema"}

    product_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(JSON)



class FeatureToProductsORM(Base):
    __tablename__ = 'FeatureToProducts'
    __table_args__ = {"schema": "clients_schema"}

    feature_to_products_id = mapped_column(Integer, primary_key=True)
    feature_product_id = mapped_column(Integer, ForeignKey('clients_schema.FeatureProduct.feature_product_id'))
    product_id = mapped_column(Integer, ForeignKey('clients_schema.Products.product_id'))

    feature_product = relationship("FeatureProductORM", backref="feature_to_products")
    product = relationship("ProductsORM", backref="feature_associations")
