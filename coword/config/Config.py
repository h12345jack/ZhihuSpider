#coding=utf8
'''
配置文件
'''
import os


QUESTION_DATA_DIR = './data/question'
if not os.path.exists(QUESTION_DATA_DIR):
    os.mkdir(QUESTION_DATA_DIR)

ANSWER_DATA_DIR = './data/answers'
if not os.path.exists(ANSWER_DATA_DIR):
    os.mkdir(ANSWER_DATA_DIR)

SPSS_DATA_DIR = './spss_data'
if not os.path.exists(SPSS_DATA_DIR):
    os.mkdir(SPSS_DATA_DIR)



QUESTION_SQL ='''
select zhihu_question.q_id, zhihu_question.q_title, zhihu_question.q_des,
       zhihu_question.q_view_num, zhihu_question.q_follow_num, zhihu_question.q_answer_num,
       zhihu_question.q_topic, log.log_max_time, log.log_min_time, log.log_count_num
       from zhihu_question left join (select q_id, min(zhihu_log.action_time) as log_min_time,max(zhihu_log.action_time) as log_max_time,
                                        count(action_id) as log_count_num from zhihu_log group by q_id) as log on(zhihu_question.q_id = log.q_id)
'''

MYSQL_CONFIG ={
    'HOST':'localhost',
    'DATABASE':'zhihu_may',
    'USER':'root',
    "PASSWORD":'admin',
    'CHARSET': 'utf8'
}