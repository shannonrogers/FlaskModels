from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Float, Table, ForeignKey, Column, Integer
from flask_marshmallow import Marshmallow



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

ma = Marshmallow()

db.init_app(app)
ma.init_app(app)

ticket_mechanic = Table(
    'ticket_mechanic', 
    Base.metadata, 
    Column('service_id', Integer, ForeignKey('services.id')), 
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'))
)

#User Model

class Customers(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)

    services: Mapped[list['Services']] = relationship('Services', back_populates='customer')

class Services(Base):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'))
    service_desc: Mapped[str] = mapped_column(String(1000), nullable=False)
    price: Mapped[float] = mapped_column(Float(15), nullable=False)
    VIN: Mapped[str] = mapped_column(String(30), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)

    mechanics: Mapped[list['Mechanics']] = relationship('Mechanics', secondary=ticket_mechanic, back_populates='services')
    customer: Mapped['Customers'] = relationship('Customers', back_populates='services')


class Mechanics(Base):
    __tablename__ = 'mechanics'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    
    services: Mapped[list['Services']] = relationship('Services', secondary=ticket_mechanic, back_populates='mechanics')


with app.app_context(): 
    db.create_all()



app.run()