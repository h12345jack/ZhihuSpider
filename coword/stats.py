#coding=utf8

import pandas as pd
from config.Config import QUESTION_DATA_DIR, ANSWER
import MySQLdb


def main():
    sql = "select * from zhihu_question"
    con = MySQLdb.connect(host="localhost", 
                          db="zhihu_may", 
                          user="root", 
                          passwd="admin", 
                          charset="utf8")
    with 
    df = pd.read_sql(sql, cons)
    for row in 