# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import time 
import re

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from scrapy.utils.serialize import ScrapyJSONEncoder

from models import ZhihuAnswerItem,ZhihuQuestionItem,ZhihuQuestionLogItem,ZhihuQuestionTask
from logfactory import piplineLogger
from settings import MYSQL_URI
from settings import DATA_STORE_DIR


# class JsonWriterPipline(object):
#     def __init__(self):
#         self.data_dir = DATA_STORE_DIR

#     def process_item(self,item,spider):
#         _encoder = ScrapyJSONEncoder()
#         line = json.dumps(json.loads(_encoder(item))) + "\n"
#         f_path = os.path.join(self.data_dir,"jsonline",q_id+'.jl')
#         with open(f_path,'a') as f:
#             f.write(line)


class DataValidatePipline(object):
    '''
    验证结果
    '''
    def process_item(self, item, spider):

        if len(item["q_data"])==0:
            raise DropItem('q_data is null')
        en_item = item["q_data"][0]
        q_entities = en_item["entities"]["questions"]
        q_id = str(item["q_id"])
        item["q_title"] = q_entities[q_id]["title"]
        item["q_des"] = q_entities[q_id]["detail"]
        item["q_view_num"] = q_entities[q_id]["visitCount"]
        item["q_follow_num"] =  q_entities[q_id]["followerCount"]
        item["q_topic"] = q_entities[q_id]["topics"]

        a_data = item["q_answer_list"]["a_data"]
        if len(a_data) == 0:
            raise DropItem('a_data is null')

        if "paging" not in a_data[0]:
            raise DropItem("a_data[0] has no paging ")

        totals = a_data[0]["paging"]["totals"]
        item["q_answer_num"] = totals


        data_totals = sum([len(i["data"]) for i in a_data])

        if totals - data_totals> 10:
            raise DropItem("data numbers don't match")
        print q_id, 'DataValidatePipline'
        return item 



class MySQLWritePipline(object):

    def __init__(self):
        self.engine = create_engine(MYSQL_URI)
        self.Session = sessionmaker(bind= self.engine)


    def add_ZhihuQuestionItem(self, item):
        return ZhihuQuestionItem(
                q_id = item["q_id"],
                q_url =  item["q_url"], 
                q_title = item["q_title"], 
                q_des = item["q_des"], 
                q_view_num = item["q_view_num"], 
                q_follow_num = item["q_follow_num"], 
                q_answer_num = item["q_answer_num"], 
                q_topic = json.dumps(item["q_topic"]),
            )

    def add_ZhihuAnswerItem(self, a_data_item, q_id):
        a_id = a_data_item["id"]
        a_qid = q_id
        a_user = a_data_item["author"]["name"]
        a_user_url = a_data_item["author"]["url"]
        a_agree_num = a_data_item["voteup_count"]
        a_content = a_data_item["editable_content"]
        a_time = a_data_item["updated_time"]
        a_thanks_num = a_data_item["thanks_count"]
        a_comment_num = a_data_item["comment_count"]

        return ZhihuAnswerItem(
                a_id = a_id,
                a_qid = a_qid,
                a_user = a_user,
                a_user_url = a_user_url,
                a_agree_num = a_agree_num,
                a_content = a_content,
                a_time = a_time,
                a_thanks_num = a_thanks_num,
                a_comment_num = a_comment_num
            )

    def add_ZhihuQuestionLogItem(self,a_log_item, q_id):
        return ZhihuQuestionLogItem(
                q_id = q_id,
                action_id= "".join(re.findall(r'[0-9]+',a_log_item["action_id"])),
                action_time =  a_log_item["action_time"], #2015-04-04 00:24:27
                action_somebody =  "".join(a_log_item["action_somebody"]),# url
                action_do =  a_log_item["action_do"],
                action_something =  a_log_item["action_something"]
            )

    def process_item(self, item, spider):
        zhihu_q_item = self.add_ZhihuQuestionItem(item)
        q_id = item["q_id"]

        zhihu_q_log_item_list = [self.add_ZhihuQuestionLogItem(i,q_id) for i in item["q_log_list"]]

        zhihu_a_list = []
        for a_json in item["q_answer_list"]["a_data"]:
            for a_answer in a_json["data"]:
                zhihu_a_list.append(self.add_ZhihuAnswerItem(a_answer,q_id))

        session = self.Session()
        zhihu_task = session.query(ZhihuQuestionTask)\
                        .filter(ZhihuQuestionTask.q_id == q_id).first()
        zhihu_task.q_finished_time = time.time()
        print q_id,"zhihu_task get" 

        try:
            session.merge(zhihu_task)
            session.merge(zhihu_q_item)
            for q_log_item in zhihu_q_log_item_list:
                print q_log_item
                session.merge(q_log_item)

            zhihu_a = session.query(ZhihuAnswerItem)\
                        .filter(ZhihuAnswerItem.a_qid == q_id).delete()
            session.add_all(zhihu_a_list)

            print q_id,"commit to DB"
            session.commit()
        except Exception as e:
            session.rollback()
            piplineLogger.error(e)
        else:
            piplineLogger.info("q_id:{} has been writed to MySQL".format(q_id))
        finally:
            session.close()

        return item



            




