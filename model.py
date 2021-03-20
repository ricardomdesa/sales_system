from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


sqliteUri = 'sqlite:///sales_db.db'
engine = create_engine(sqliteUri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Seller(Base):
    __tablename__ = 'seller'
    id = Column(Integer, primary_key=True)
    seller_name = Column(String(20), unique=True)
    amount_sales = Column(Float)

    def __repr__(self):
        return f'<Seller {self.seller_name}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('seller.id'))
    customer_name = Column(String(20))
    sale_date = Column(String(20))
    sale_name = Column(String(20))
    sale_value = Column(Float)
    seller = relationship('Seller')

    def __repr__(self):
        return f'<Sale {self.sale_name}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def add_initial_sellers():
    # check if initial sellers exists
    seller = Seller.query.filter_by(seller_name='John').first()
    if not seller:
        seller1 = Seller(seller_name='John', amount_sales=0)
        seller1.save()
        seller2 = Seller(seller_name='Peter', amount_sales=0)
        seller2.save()
        seller3 = Seller(seller_name='Maria', amount_sales=0)
        seller3.save()
        seller4 = Seller(seller_name='Patricia', amount_sales=0)
        seller4.save()
        seller5 = Seller(seller_name='Ricardo', amount_sales=0)
        seller5.save()


def init_db():
    Base.metadata.create_all(bind=engine)
    add_initial_sellers()