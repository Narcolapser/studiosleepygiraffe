from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime

engine = create_engine('sqlite:///ssg.sqlite',echo=True)
Session = sessionmaker(bind=engine)


def log_visit(request):
    print("Got a request from {} for {} at {}".format(request.remote_addr,request.path,datetime.now()))
    v = Visit(ip=request.remote_addr,time=datetime.now(),url=request.path)

    session = Session()
    session.add(v)
    session.commit()


Base = declarative_base()


class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True)

    ip = Column(String)
    time = Column(DateTime)
    url = Column(String)


Base.metadata.create_all(engine)
