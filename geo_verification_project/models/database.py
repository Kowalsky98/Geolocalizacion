# models/database.py
from sqlalchemy import create_engine, Column, String, Boolean, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class GeoRecord(Base):
    __tablename__ = 'georecords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    serial = Column(String, nullable=False)
    alert = Column(Boolean, nullable=False)
    alert_type = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

engine = create_engine('postgresql://user:password@localhost/geodb')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
