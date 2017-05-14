#coding=utf8

import json
import jieba
import os
import re
import time
import codecs
from collections import defaultdict

import lxml.html
import jieba.analyse
import MySQLdb
import pandas as pd


from config.Config import QUESTION_DATA_DIR, ANSWER_DATA_DIR, MIDDLE_DATA
from config.Config import STOPWORD, TOPICDICT, QUESTION_TOPIC

from config.Config import ANSWER_JSONLINE, ANSWERS_TXT_DATA_DIR

from config.Config import CUT_WORD_DIC


question_file = "zhihu_question.jl"

answer_file = "zhihu_answer.jl"



def question_dict_gen():
    '''
    读取question_topic的数据作为默认词典
    '''
    f = codecs.open(QUESTION_TOPIC, 'r', 'utf8')
    question_dict = set()
    for line in f.readlines():
        word_list = line.strip().split(',')
        for word in word_list:
            # 优步（Uber）
            w1 = re.findall(u"(.*)\s*（(.*)）",word)
            if len(w1) > 0:
                for i in w1[0]:
                    if i not in question_dict:
                        print i,"w1"
                        question_dict.add(i)
            else:
                w2 = re.findall(r'(.*)\s*\((.*)\)',word)
                if len(w2) > 0: 
                    for i in w2[0]:
                        print i,"w2"
                        question_dict.add(i)
                else:
                    w3 = word.split()
                    if len(w3) > 1:
                        for i in w3:
                            print i,"w3"
                            question_dict.add(i)

            if word not in question_dict:
                question_dict.add(word)
    f = file(TOPICDICT,'w')
    for word in question_dict:
        f.write(word.encode('utf8')+'\n')

def question_dict_gen2():
    '''
    相比之间的函数，多了一个统计功能
    '''
    f = codecs.open(QUESTION_TOPIC, 'r', 'utf8')
    question_dict = defaultdict(int)
    for line in f.readlines():
        word_list = line.strip().split(',')
        for word in word_list:
            # 优步（Uber）
            w1 = re.findall(u"(.*)\s*（(.*)）",word)
            if len(w1) > 0:
                for i in w1[0]:
                    question_dict[i] += 1
            else:
                w2 = re.findall(r'(.*)\s*\((.*)\)',word)
                if len(w2) > 0: 
                    for i in w2[0]:
                        question_dict[i] += 1
                else:
                    w3 = word.split()
                    if len(w3) > 1:
                        for i in w3:
                            question_dict[i] += 1
            question_dict[word] += 1
    f = file(TOPICDICT+'2','w')
    item_list = sorted(question_dict.items(), key= lambda x:x[1], reverse=True)
    for item in item_list:
        f.write(item[0].encode('utf8')+','+str(item[1])+'\n')



def step1():
    question_dict_gen()
    question_dict_gen2()


def step2():
    '''
    将回答的内容导出到answers_data文件夹中，然后调用切词工具包即可
    这个方法非常的慢！不要轻易尝试

    '''
    a_id_duplicate = set()
    i = 0
    last_time = time.time()
    with codecs.open(ANSWER_JSONLINE) as f:
        for line in f.readlines():
            i += 1
            json_data = json.loads(line.strip())
            a_id = json_data["a_id"]
            # if a_id not in a_id_duplicate:
            #     a_id_duplicate.add(a_id)
            # else:
            #     print a_id, 'duplicated!'

            ## 写出文件
            file_path = os.path.join(ANSWERS_TXT_DATA_DIR, a_id + '.txt')
            with open(file_path, 'w') as output:
                output.write(json_data["a_content"].encode("utf8"))
            if i % 1000 ==0: 
                print i, 'write 2 txt', "use", time.time() - last_time
                last_time = time.time()

def step3():
    '''
    统计各种切词工具的结果
    '''
    tools_dic = CUT_WORD_DIC
    for tool_name in tools_dic:
        print tool_name, 'stats'
        data_dir = tools_dic[tool_name]
        file_list = os.listdir(data_dir)
        corpus=[]
        stats=defaultdict(int)
        for filename in file_list:
            filename = os.path.join(data_dir,filename)
            f=codecs.open(filename,'r','utf8')
            for line in f.readlines():
                word = line.strip()
                stats[word] += 1

        rs=sorted(stats.iteritems(), key=lambda x:x[1], reverse=True)
        f2=file(os.path.join(MIDDLE_DATA, tool_name + '_word_stats.txt'), 'w')
        num=0
        for i in rs:
            if i[1]==1:num+=1
            f2.write(i[0].encode('utf8')+','+str(i[1])+'\n')

        print tool_name,'all word:',len(rs), 'freq = 1:', num


def test():
    # stop_list = read_stopword()
    step3()

def main():
    test()
    print 'end'


if __name__ == '__main__':
    main()