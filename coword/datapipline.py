#coding=utf8
import os
import re
import json

import pandas as pd
import MySQLdb
import lxml.html as html

from config.Config import QUESTION_DATA_DIR, ANSWER_DATA_DIR, SPSS_DATA_DIR
from config.Config import QUESTION_SQL,MYSQL_CONFIG


def extract_content_info(content):
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


def output_raw_question_data():
    '''
    提取出jsonline的数据
    q_id    q_url   q_title q_des   q_view_num  q_follow_num    q_answer_num    q_topic
    原始的数据，不做清洗
    '''
    table_name = "zhihu_question"
    sql = QUESTION_SQL
    con = MySQLdb.connect(host=MYSQL_CONFIG["HOST"], 
                          db=MYSQL_CONFIG["DATABASE"], 
                          user=MYSQL_CONFIG["USER"], 
                          passwd=MYSQL_CONFIG["PASSWORD"], 
                          charset=MYSQL_CONFIG["CHARSET"])

    df = pd.read_sql(sql, con)
    excel_path = os.path.join(SPSS_DATA_DIR,table_name+'_raw.xlsx')
    df.to_excel(excel_path)
    print excel_path, 'done'

    output_file = os.path.join(QUESTION_DATA_DIR,table_name+'_raw.jl')
    with open(output_file,'w') as f:
        for row in df.iterrows():
            row[1].to_json(f)
            f.write('\n')
    print output_file, 'done'


def output_clean_question_data():
    '''
    将question数据导出
    '''
    input_excel = os.path.join(SPSS_DATA_DIR, 'zhihu_question_raw.xlsx')
    df = pd.read_excel(input_excel)
    #冗余计算
    real_content_func = lambda x: extract_content_info(x)[0]
    img_func = lambda x:extract_content_info(x)[1]
    a_func = lambda x:extract_content_info(x)[2]
    topic_list = lambda x:",".join(extract_topic_list(x))
    topic_list_num = lambda x:len(extract_topic_list(x))

    df["real_des"] = df["q_des"].apply(real_content_func)
    df["real_des_num"] = df["real_des"].apply(lambda x:len(x))
    df["title_num"] = df["q_title"].apply(lambda x:len(x))
    df["des_img_num"] = df["q_des"].apply(img_func)
    df["des_a_num"] = df["q_des"].apply(a_func)
    df["topic_list"] = df["q_topic"].apply(topic_list)
    df["topic_list_num"] = df["q_topic"].apply(topic_list_num)

    print 'apply end','write 2 zhihu_question_clean.xlsx'
    excel_path = os.path.join(SPSS_DATA_DIR, "zhihu_question_clean.xlsx")
    df.to_excel(excel_path)
    print excel_path, 'done'

    output_file = os.path.join(QUESTION_DATA_DIR,'zhihu_question_clean.jl')
    with open(output_file,'w') as f:
        for row in df.iterrows():
            row[1].to_json(f)
            f.write('\n')
    print output_file, 'done'


def output_raw_answer_data():
   
    table_name = "zhihu_answer"
    sql = QUESTION_SQL
    con = MySQLdb.connect(host=MYSQL_CONFIG["HOST"], 
                          db=MYSQL_CONFIG["DATABASE"], 
                          user=MYSQL_CONFIG["USER"], 
                          passwd=MYSQL_CONFIG["PASSWORD"], 
                          charset=MYSQL_CONFIG["CHARSET"])
    sql = "select * from zhihu_answer"
    df = pd.read_sql(sql, con)
    excel_path = os.path.join(SPSS_DATA_DIR,table_name+'_raw.xlsx')
    # df.to_excel(excel_path)
    print 'df to excel IGNORE',excel_path

    output_file = os.path.join(ANSWER_DATA_DIR,table_name+'_raw.jl')
    with open(output_file,'w') as f:
        for row in df.iterrows():
            row[1].to_json(f)
            f.write('\n')
    print 'df to jsonline done', output_file


def output_clean_answer_data():

    table_name = "zhihu_answer"
    raw_data_path = os.path.join(ANSWER_DATA_DIR, table_name+'_raw.jl')
    f = file(raw_data_path)

    clean_data_path = os.path.join(ANSWER_DATA_DIR, table_name+'_clean.jl')
    output_f = file(clean_data_path,'w')

    for line in f.readlines():
        json_data = json.loads(line.strip())
        content = json_data["a_content"]
        try:
            answer_real_content, answer_img_num, answer_a_num = extract_content_info(content)
        except Exception as e:
            print json_data["a_id"],e
            continue
        json_data["a_content"] = answer_real_content
        json_data["answer_img_num"] = answer_img_num
        json_data["answer_a_num"] = answer_a_num
        output_f.write(json.dumps(json_data)+"\n")
    print clean_data_path, 'done'


def test():
    output_raw_question_data()
    print 'output raw question done!'
    output_clean_question_data()
    print 'output clean question done!'
    output_raw_answer_data()
    print 'output raw answer done!'
    output_clean_answer_data()
    print 'output clean answer done!'

def main():
    test()

if __name__ == '__main__':
    main()