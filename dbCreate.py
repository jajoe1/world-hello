from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///test3.db', echo=True)
Base = declarative_base()



class Device(Base):
    """"""
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    cat = Column(String)
    name = Column(String)

class Host(Base):
    """"""
    __tablename__ = "host"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    customer = Column(Boolean)
    engineering = Column(Boolean)
    extra = Column(String)




# create tables
Base.metadata.create_all(engine)
