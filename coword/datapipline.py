#coding=utf8
import os
import re
import json

import pandas as pd
import MySQLdb
import lxml.html as html

from config.Config import QUESTION_DATA_DIR, ANSWER_DATA_DIR, SPSS_DATA_DIR
from config.Config import QUESTION_SQL,MYSQL_CONFIG




def output_question_jsonline():
    '''
    提取出jsonline的数据
    q_id    q_url   q_title q_des   q_view_num  q_follow_num    q_answer_num    q_topic

    '''
    table_name = "zhihu_question"
    sql = QUESTION_SQL
    con = MySQLdb.connect(host=MYSQL_CONFIG["HOST"], 
                          db=MYSQL_CONFIG["DATABASE"], 
                          user=MYSQL_CONFIG["USER"], 
                          passwd=MYSQL_CONFIG["PASSWORD"], 
                          charset=MYSQL_CONFIG["CHARSET"])

    df = pd.read_sql(sql, con)
    excel_path = os.path.join(SPSS_DATA_DIR,table_name+'.xlsx')
    df.to_excel(excel_path)

    output_file = os.path.join(QUESTION_DATA_DIR,table_name+'.jl')
    with open(output_file,'w') as f:
        for row in df.iterrows():
            row[1].to_json(f)
            f.write('\n')

def extract_hyper_link(content):
    '''
    img:src
    a: href
    '''
    if pd.isnull(content):
        content = ""
    if isinstance(content, int):
        content = str(content)
    # content = str(content.decode("utf8"))
    content = "<div>"+content+"</div>"

    node = html.fromstring(content)
    real_content = "".join([i.strip() for i in node.xpath("//text()") if i.find("http://")==-1])
    real_content = real_content.strip()

    img_src_xpath = '//img/@src'
    img_xpath = '//img'
    img_num1 = len(node.xpath(img_xpath))
    img_num2 = len(node.xpath(img_src_xpath))
    assert img_num1 == img_num2, 'img num is not same'

    a_xpath = '//a'
    a_href_xpath = '//a/@href'
    a_num1 = len(node.xpath(a_xpath))
    a_num2 = len(node.xpath(a_href_xpath))
    assert a_num1 == a_num2, 'a number is not same'

    return (real_content, img_num1, a_num1)

def extract_topic_list(content):
    json_data = json.loads(str(content))
    return [i["name"] for i in json_data]


def to_question_spss_xlsx():
    '''
    将question数据导出
    '''
    input_excel = os.path.join(SPSS_DATA_DIR, 'zhihu_question.xlsx')
    df = pd.read_excel(input_excel)
    #冗余计算
    real_content_func = lambda x: extract_hyper_link(x)[0]
    img_func = lambda x:extract_hyper_link(x)[1]
    a_func = lambda x:extract_hyper_link(x)[2]
    topic_list = lambda x:",".join(extract_topic_list(x))
    topic_list_num = lambda x:len(extract_topic_list(x))

    df["real_des"] = df["q_des"].apply(real_content_func)
    df["real_des_num"] = df["real_des"].apply(lambda x:len(x))
    df["title_num"] = df["q_title"].apply(lambda x:len(x))
    df["des_img_num"] = df["q_des"].apply(img_func)
    df["des_a_num"] = df["q_des"].apply(a_func)
    df["topic_list"] = df["q_topic"].apply(topic_list)
    df["topic_list_num"] = df["q_topic"].apply(topic_list_num)

    print 'apply end','write 2 zhihu_question_spss.xlsx'
    df.to_excel("zhihu_question_spss.xlsx")

def extract_answer():
   
    table_name = "zhihu_answer"
    sql = QUESTION_SQL
    con = MySQLdb.connect(host=MYSQL_CONFIG["HOST"], 
                          db=MYSQL_CONFIG["DATABASE"], 
                          user=MYSQL_CONFIG["USER"], 
                          passwd=MYSQL_CONFIG["PASSWORD"], 
                          charset=MYSQL_CONFIG["CHARSET"])
    sql = "select * from zhihu_answer"
    df = pd.read_sql(sql, con)
    excel_path = os.path.join(SPSS_DATA_DIR,table_name+'.xlsx')
    # df.to_excel(excel_path)
    print 'df to excel IGNORE',excel_path
    output_file = os.path.join(ANSWER_DATA_DIR,table_name+'.jl')
    with open(output_file,'w') as f:
        for row in df.iterrows():
            row[1].to_json(f)
            f.write('\n')
    print 'df to jsonline done', output_file

def test():
    output_question_jsonline()
    to_question_spss_xlsx()

def main():
    extract_answer()

if __name__ == '__main__':
    main()