from sqlalchemy import Column, Integer, JSON, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.src.database import Base


class GroupProduct(Base):
    __tablename__ = 'GroupProduct'

    group_product_id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(200))
    type = Column(String(200))
    status = Column(String(200))
    name = Column(String(200))
    title = Column(JSON)
    descr = Column(JSON)
    custom = Column(JSON)
    prices = Column(JSON)
    image = Column(JSON)

    products = relationship("Products", secondary="GroupToProducts", backref="groups")
    channels = relationship('Channel', secondary='Channel_GroupProduct', backref='products')


class FeatureProduct(Base):
    __tablename__ = 'FeatureProduct'

    feature_product_id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(200))
    status = Column(String(200))
    name = Column(String(200))
    quota = Column(Integer)
    valid_period = Column(Integer)
    title = Column(JSON)
    descr = Column(JSON)
    custom = Column(JSON)
    prices = Column(JSON)
    image = Column(JSON)

    products = relationship("Products", secondary="FeatureToProducts", backref="features")


class Products(Base):
    __tablename__ = 'Products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(JSON)


class GroupToProducts(Base):
    __tablename__ = 'GroupToProducts'

    group_to_products_id = Column(Integer, primary_key=True, autoincrement=True)
    group_product_id = Column(Integer, ForeignKey('GroupProduct.group_product_id'))
    product_id = Column(Integer, ForeignKey('Products.product_id'))

    group_product = relationship("GroupProduct", backref="group_to_products")
    product = relationship("Products", backref="group_associations")


class FeatureToProducts(Base):
    __tablename__ = 'FeatureToProducts'

    feature_to_products_id = Column(Integer, primary_key=True, autoincrement=True)
    feature_product_id = Column(Integer, ForeignKey('FeatureProduct.feature_product_id'))
    product_id = Column(Integer, ForeignKey('Products.product_id'))

    feature_product = relationship("FeatureProduct", backref="feature_to_products")
    product = relationship("Products", backref="feature_associations")
