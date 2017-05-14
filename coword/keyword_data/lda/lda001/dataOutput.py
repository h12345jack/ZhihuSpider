#coding=utf8
import os

from collections import defaultdict

import gensim
from gensim.models import LdaModel

t_num_list = [50, 100, 400]

DOT_V = 1500 * 100

def main():
    for t_num in t_num_list:
        LDA1_FILE = './lda1_topic_{}/jieba_lda.data'.format(t_num)
        res_dict = defaultdict(float)
        lda = LdaModel.load(LDA1_FILE)

        for i in lda.show_topics(num_topics = t_num, num_words= DOT_V/t_num, formatted = False):
            doc_id = i[0]
            rs_tuple_list = i[1]
            print rs_tuple_list[-1]
            for t in rs_tuple_list:
                res_dict[t[0]] += t[1]

        item_list = sorted(res_dict.iteritems(), key = lambda x: x[1], reverse=True)
        rs_f = file('lda1_topic{}.txt'.format(t_num),'w')
        for i in item_list:
            print>>rs_f, i[0].encode("utf8")+','+str(i[1])


if __name__ == '__main__':
    main()