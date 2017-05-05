# -*- coding:utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import MYSQL_URI
from models import Base
engine = create_engine(MYSQL_URI)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def initDb():
    """
        生成数据库表
    :return:
    """
    Base.metadata.create_all(engine)

def dropDb():
    """
        删除数据库表
    :return:
    """
    Base.metadata.drop_all(engine)


if  __name__ == "__main__":
    initDb()