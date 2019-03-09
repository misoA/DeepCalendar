# -*- coding: utf-8 -*-
from sqlalchemy import MetaData, Table
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# DB Model Auto Generate
engine = create_engine('mysql://{USER_NAME}:{PASSWORD}@{DB_END_POINT}:{DB_PORT}/{DB_NAME}?charset=utf8', echo=False)
metadata = MetaData(bind=engine)

class BPCustomer(Base):
    __table__ = Table('BPCustomer', metadata, auto_increment=False, autoload=True)

class BPRating(Base):
    __table__ = Table('BPRating', metadata, auto_increment=True, autoload=True)

class Calendar(Base):
    __table__ = Table('Calendar', metadata, auto_increment=True, autoload=True)
    
class Closet(Base):
    __table__ = Table('Closet', metadata, auto_increment=True, autoload=True)
    
class Code(Base):
    __table__ = Table('Code', metadata, auto_increment=False, autoload=True)

class CodeTag(Base):
    __table__ = Table('CodeTag', metadata, auto_increment=True, autoload=True)
    
class GoodsOption(Base):
    __table__ = Table('GoodsOption', metadata, auto_increment=True, autoload=True)
    
class GoodsTag(Base):
    __table__ = Table('GoodsTag', metadata, auto_increment=False, autoload=True)
    
class MusinsaCustomer(Base):
    __table__ = Table('MusinsaCustomer', metadata, auto_increment=False, autoload=True)
    
class MusinsaGoods(Base):
    __table__ = Table('MusinsaGoods', metadata, auto_increment=False, autoload=True)
  
class RecommendGoods(Base):
    __table__ = Table('RecommendGoods', metadata, auto_increment=True, autoload=True)
    
class MusinsaReview(Base):
    __table__ = Table('MusinsaReview', metadata, auto_increment=True, autoload=True)
    
class SsmkGoods(Base):
    __table__ = Table('SsmkGoods', metadata, auto_increment=True, autoload=True)
    
class WeatherCode(Base):
    __table__ = Table('WeatherCode', metadata, auto_increment=False, autoload=True)
    
