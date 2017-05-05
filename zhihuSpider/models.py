#-*- coding:utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ZhihuQuestionTask(Base):
    __tablename__ = 'zhihu_question_task'

    q_id = Column(Integer,primary_key = True)
    q_url = Column(String(250),unique = True)
    q_create_time = Column(Integer)
    q_finished_time = Column(Integer)

class ZhihuQuestionItem(Base):
    __tablename__ = 'zhihu_question'

    q_id = Column(String(20),primary_key = True)
    q_url =  Column(String(250), unique=True)
    q_title = Column(String(1000))#question title
    q_des = Column(Text)# question description
    q_view_num = Column(Integer) #被浏览 157885 次
    q_follow_num =  Column(Integer) #5567 人关注该问题
    q_answer_num =  Column(Integer) #25 个回答
    q_topic = Column(Text) # topic的(topic,url)

class ZhihuAnswerItem(Base):
    __tablename__ = 'zhihu_answer'
    
    a_id = Column(String(20),primary_key = True)
    a_qid = Column(String(20))
    a_user = Column(String(100)) # username url
    a_user_url = Column(String(250))
    a_agree_num = Column(Integer) #赞同数量
    a_content = Column(Text) 
    a_time = Column(Integer)#时间
    a_comment_num = Column(Integer) #评论数量
    a_thanks_num = Column(Integer)

class ZhihuQuestionLogItem(Base):
    __tablename__ = 'zhihu_log'

    q_id = Column(Integer) 
    action_id= Column(String(20),primary_key=True) # #113421760
    action_time =  Column(String(200)) #2015-04-04 00:24:27
    action_somebody =  Column(String(100)) # url
    action_do =  Column(String(20)) #移除了话题
    action_something =  Column(Text) # 包括后面的修改理由

