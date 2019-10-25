import datetime as dt

import pytz as pytz
from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey, MetaData, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


def get_utc_time():
    utc_tz = pytz.timezone('UTC')
    return utc_tz.localize(dt.datetime.utcnow())


meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })

Base = declarative_base(metadata=meta)


class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    host = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    sponsor = Column(String)
    url = Column(String)
    distance_km = Column(Float)
    country_code = Column(String)


class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    server_id = Column(ForeignKey('servers.id'),
                       nullable=False,
                       index=True)
    download_bps = Column(Float)
    upload_bps = Column(Float)
    ping_ms = Column(Float)
    bytes_received = Column(Integer)
    bytes_sent = Column(Integer)
    server_latency = Column(Float)
    ip = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    test_time = Column(DateTime(timezone=True), default=get_utc_time)

    server = relationship(Server)
