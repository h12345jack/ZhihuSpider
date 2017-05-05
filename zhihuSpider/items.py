#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ZhihuQuestionItem(Item):
    q_id = Field()
    q_url = Field()
    
    q_title = Field()#question title
    q_des = Field()# question description
    q_view_num = Field() #被浏览 157885 次
    q_follow_num =  Field() #5567 人关注该问题
    q_answer_num =  Field() #25 个回答
    q_topic = Field() # topic的(topic,url)
    q_answer_list = Field()
    q_data = Field()
    q_log_list = Field()

class ZhihuAnswerItem(Item):
    a_url = Field()
    a_user = Field() # username url
    a_user_url = Field() #user url
    a_agree_num = Field() #赞同数量
    a_content = Field() 
    a_time = Field()#时间
    a_comment_num = Field() #评论数量
    a_data = Field()
    

class ZhihuQuestionLogItem(Item):
    action_id=Field() # #113421760
    action_time = Field() #2015-04-04 00:24:27
    action_somebody = Field() # url
    action_do = Field() #移除了话题
    action_something = Field() # 包括后面的修改理由
'''
# poem 移除了话题
# 喃字
# #197400925 •撤销 •举报恶意编辑 •2015-09-19 12:47:39
# https://www.zhihu.com/question/29077330/log
# sleeping knight 编辑了补充说明
# 看着一只只原本受伤可怜的小猫在精心照顾下都变成了家里的老大，真的觉得心里暖暖的。

# 有可能是外表的变化，也有可能是心理的一些变化。

# 这也是一个炫猫帖(〃ﾉωﾉ)
# ===
# 原问题只问了猫，发现有些知友也想分享其他动物的经历，故修改
# 修改理由：补充必要的信息
# #113421760 •撤销 •举报恶意编辑 •2015-04-04 00:24:27


# '''

# class ZhihuQuestionItem(Item):
#     q_url = Field()#question url
#     q_title = Field()#question title
#     q_des = Field()# question description
#     q_view_num = Field() #被浏览 157885 次
#     q_answer_num =  Field() #25 个回答
#     q_follower_num =  Field() #5567 人关注该问题
#     q_topic = Field() # topic的url列表 统计次数。
#     q_answer_list = Field() #回答的列表
#     #新增的部分
#     q_related_q=Field() #相关问题 url+num
#     q_log=Field() #list



# class ZhihuAnswerItem(Item):
#     a_user_url = Field()
#     a_user_name = Field()
#     a_agree_num = Field() #赞同数量
#     a_content = Field() 
#     a_time = Field()#时间
#     a_comment_num = Field() #评论数量
#     a_comment_list = Field() #评论list
#     a_url = Field()

# class ZhihuCommentItem(Item):
#     c_A2B=Field()
#     c_content = Field()
#     c_time = Field()
#     c_agree_num = Field()


