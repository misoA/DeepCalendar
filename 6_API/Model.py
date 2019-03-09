from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import config

ma = Marshmallow()
db = SQLAlchemy()

from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, encoding='utf8', echo=False)
metadata = MetaData(bind=engine)
    
    
class BPRating(Base):
    __table__ = Table('BPRating', metadata, auto_increment=True, autoload=True)

class BPCustomer(Base):
    __table__ = Table('BPCustomer', metadata, auto_increment=False, autoload=True)

class RecommendGoods(Base):
    __table__ = Table('RecommendGoods', metadata, auto_increment=True, autoload=True)