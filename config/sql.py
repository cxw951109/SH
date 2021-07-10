import json
import time
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String,Integer,create_engine

engine = create_engine('mysql+pymysql://root:1111@localhost:3306/sh',pool_size=10)

Base = declarative_base()


def get_datas():
    session2 = MySession()
    query = session2.query(Dailydata).first()
    session2.close()
    if query:
        all =query.goodNum+query.badNum
        return all,query.goodNum,query.badNum
    else:
        return 0,0,0


class Dailydata(Base):
    __tablename__ = 'daily_data'

    id = Column(Integer(), primary_key=True,autoincrement=True)
    goodNum = Column(Integer)
    badNum = Column(Integer)
    created_time = Column(String(20))


Base.metadata.create_all(engine)

MySession = sessionmaker(bind=engine)
session = MySession()
t = time.strftime("%Y-%m-%d",time.localtime())
try:
    res = session.query(Dailydata).first()
    if not res:
        session.add(Dailydata(goodNum=0, badNum=0,created_time =t))
        session.commit()
    else:
        if res.created_time ==t:
            pass
        else:
            session.query(Dailydata).update({Dailydata.badNum:0,Dailydata.goodNum:0,Dailydata.created_time:t},synchronize_session=False)   
            session.commit()
    session.close()     
except:
    pass

