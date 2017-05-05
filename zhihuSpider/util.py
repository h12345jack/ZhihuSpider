#coding=utf8
import time
import re
import random


import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import MYSQL_URI
from models import ZhihuQuestionTask,Base
from settings import NEED_CRAWL_URL_FILE


engine = create_engine(MYSQL_URI)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def initDb():
    """
        生成数据库表
    :return:
    """
    Base.metadata.create_all(engine)

def addTask(url):
    q_id = re.findall(r"[0-9]+",url)
    assert len(q_id)>0, u"url中无数字"
    q_url = url.strip()
    q_create_time = time.time()
    return ZhihuQuestionTask(
               q_id = q_id[0],
               q_url = q_url,
               q_create_time = q_create_time,
               q_finished_time = 0)

def addAllTask():
    session = DBSession()
    task_list = []

    # task_list.append(
            #     ZhihuQuestionTask(
            #        q_id = q_id[0],
            #        q_url = q_url,
            #        q_create_time = q_create_time,
            #        q_finished_time = 0)
            # )
    # session.add_all(task_list)

    with open(NEED_CRAWL_URL_FILE) as f:
        for line in f.readlines():
            session.merge(addTask(line.strip()))
    session.commit()

def getTasks():
    '''获取url—list'''
    session = DBSession()
    tasks = session.query(ZhihuQuestionTask).from_statement(
        sqlalchemy.text("SELECT * FROM zhihu_question_task where q_finished_time=0"))
    url_list = [task.q_url for task in tasks.all()]
    return url_list


def time_sleep_random(a,b):
    '''
    随机休息a-b之间的随机数
    '''
    ran = random.uniform(a,b)
    print "sleep",ran/2
    time.sleep(ran/2)

def updateTask(q_id):
    session = DBSession()
    zhihu_task = session.query(ZhihuQuestionTask)\
                        .filter(ZhihuQuestionTask.q_id == q_id).first()
    zhihu_task.q_finished_time = -1
    session.merge(zhihu_task)
    session.commit()

def main():
    initDb()
    addAllTask()
    print len(getTasks())
    updateTask("19556316")

if __name__ == '__main__':
    main()
