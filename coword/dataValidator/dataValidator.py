#coding=utf8


import os
import re
from collections import defaultdict
import codecs
'''
统计标注的数据，计算 准确率和召回率
'''


from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import recall_score, roc_auc_score
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd


EXCEL_FILE = './data.xlsx'
JIEBA_POS_FILE = './jieba_pos_word_stats.txt'
MEASURE_EXCEL_FILE = './method_messure.xlsx'
allow_pos1 = ['ns', 'nr', 'ng', 'nt', 'nz','n','x','v','vn',
             'a', 'an', 'eng', 'i', 'j', 'l', 's', 't']

allow_pos2 = ['ns', 'nr', 'ng', 'nt', 'nz', 'n', 'x' ]

allow_pos3 = ['ns', 'nr', 'ng', 'nt', 'nz', 'n']

def getTermList():
    rs_dict = defaultdict(int)
    with open(JIEBA_POS_FILE) as f:
        for line in f.readlines():
            line = line.strip().split(',')
            if len(line)>2:
                rs_dict[line[0]+'_'+line[1]] += int(line[2])
    return rs_dict


def is_Contained(term, my_dict, flag=1):
    '''
    判断该词是否保留
    '''
    if flag == 1:
        for pos in allow_pos1:
            term2 = term + '_' +pos
            term2 = term2.encode('utf8')
            # print term2, term2 == '希望_v'
            if term2 in my_dict and my_dict[term2] > 5:
                print term2
                return 1
        return 0
    elif flag == 2:
        for pos in allow_pos2:
            term2 = term + '_' +pos
            term2 = term2.encode('utf8')
            # print term2, term2 == '希望_v'
            if term2 in my_dict and my_dict[term2] > 5:
                print term2
                return 1
        return 0
    else:
        print flag
        for pos in allow_pos3:
            term2 = term + '_' +pos
            term2 = term2.encode('utf8')
            # print term2, term2 == '希望_v'
            if term2 in my_dict and my_dict[term2] > 5:
                print term2
                return 1
        return 0





def getValidateTopN(term_list, term_dict, col, flag = 1, topn = 400):
    result = []
    for term in term_list:
        if is_Contained(term, term_dict, flag):
            result.append(term)

    assert len(result) >= topn, col+'term not enough!'
    return result[:topn]



def main():

    term_dict = getTermList()

    execel = pd.read_excel(EXCEL_FILE)
    topic_list = execel["topic_list"].tolist()
    rs_dict = dict()
    all_set = set()

    method_list = [
        "freq1", "textrank1","textrank2", "tfidf1", "tfidf2",
        "lda001-50", "lda001-100", "lda001-400",
        "lda002-50", "lda002-100", "lda002-400"
    ]

    for col in method_list:
        col_series = [str(i) if isinstance(i, float) or isinstance(i, int) else i.strip() for i in execel[col].tolist()]
        print col, "="*100
        topn = getValidateTopN(col_series, term_dict, col, 1, 400)
        all_set = all_set | set(topn)
        rs_dict[col+'_poslimit1'] = topn

    for col in method_list:
        col_series = [str(i) if isinstance(i, float) or isinstance(i, int) else i.strip() for i in execel[col].tolist()]
        print col, "="*100
        topn = getValidateTopN(col_series, term_dict, col, 2, 400)
        all_set = all_set | set(topn)
        rs_dict[col+'_poslimit2'] = topn

    for col in method_list:
        col_series = [str(i) if isinstance(i, float) or isinstance(i, int) else i.strip() for i in execel[col].tolist()]
        print col, "="*100
        topn = getValidateTopN(col_series, term_dict, col, 3, 400)
        all_set = all_set | set(topn)
        rs_dict[col+'_poslimit3'] = topn

    all_union = list(all_set)
    with open('all_union.txt','w') as f_all_union:
        for i in all_union:
            print>>f_all_union, str(i) if isinstance(i, int) else i.encode('utf8')
    df = pd.DataFrame.from_dict(rs_dict)
    df.to_excel("data_handled.xlsx")



def main():
    pass


def map_cal():
    df = pd.read_excel(MEASURE_EXCEL_FILE)
    method_list = [
        "freq1","freq1_poslimit1","freq1_poslimit2","freq1_poslimit3",
        "lda001-100_poslimit1","lda001-100_poslimit2","lda001-100_poslimit3",
        "lda001-400_poslimit1","lda001-400_poslimit2","lda001-400_poslimit3",
        "lda001-50_poslimit1","lda001-50_poslimit2","lda001-50_poslimit3",
        "lda002-100_poslimit1","lda002-100_poslimit2","lda002-100_poslimit3",
        "lda002-400_poslimit1","lda002-400_poslimit2","lda002-400_poslimit3",
        "lda002-50_poslimit1","lda002-50_poslimit2","lda002-50_poslimit3",
        "textrank1","textrank2",
        "tfidf1_poslimit1","tfidf1_poslimit2","tfidf1_poslimit3",
        "tfidf2_poslimit1","tfidf2_poslimit2","tfidf2_poslimit3"
    ]
    for method in method_list:
        m_list_o = df[method].tolist()
        k_list = [10, 50, 100, 400]
        for k in k_list:
            m_list = m_list_o[:k]
            map_s = []
            s = 0
            for i, v in enumerate(m_list):
                if int(v) == 1:
                    s += 1
                    map_s.append(float(s)/(i+1))
            print method, k, np.array(map_s).mean(), np.array(m_list).sum()


def test():
    map_cal()







if __name__ == '__main__':
    test()




