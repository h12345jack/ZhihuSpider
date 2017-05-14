#coding=utf8


# coding=utf8

import os
import codecs
import json
import re
from collections import defaultdict

import jieba
import jieba.analyse

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

from gensim import corpora, models, similarities
from gensim.models import LdaModel
from gensim.models import TfidfModel

DATA_DIR = './cut_word_tools/answers_data'
JIEBA_DIR = './cut_word_tools/jieba_data'
TEXT_RANK_DATA = './keyword_data/text_rank'
USER_DICT = './cut_word_tools/user_dict.txt'
STOP_WORD = './cut_word_tools/stop_word.txt'

JIEBA_LDA_MODLE = './jieba_lda.data'
JIEBA_LDA_MODEL2 = './jieba_lda2.data'

QUETSION_BASED_DIR = '../question_based'


def is_stopword(stop_word, word):
    return word in stop_word


def lda_main1():
    # f_list=["100002481.txt","100003106.txt"]
    topic_num = 2000
    f_list = os.listdir(JIEBA_DIR)
    f_list = [os.path.join(JIEBA_DIR, i) for i in f_list]

    def f(filename):
        content = codecs.open(filename, 'r', 'utf8')
        word_list = [line.strip() for line in content.readlines()]
        return word_list

    words = [f(i) for i in f_list]
    # print words[1]
    dic = corpora.Dictionary(words)
    corpus = [dic.doc2bow(text) for text in words]
    print 'LDA TRAINING', topic_num

    # lda模型训练
    lda = LdaModel(corpus=corpus, id2word=dic, num_topics=topic_num)
    data_dir = './lda1_topic_'+str(topic_num)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    data_path = os.path.join(data_dir, "jieba_lda.data")
    lda.save(data_path)
    rs_f = file('lda1_topic_'+str(topic_num)+'rs.txt','w')
    for i in range(lda.num_topics-1):
        print>>rs_f, lda.print_topic(i,topn = 10).encode('utf8')


# def lda_main2():
#     '''将问答视为一个文档'''
#     # f_list=["100002481.txt","100003106.txt"]
#     topic_num = 50
#     f_list = os.listdir(QUETSION_BASED_DIR)
#     f_list = [os.path.join(QUETSION_BASED_DIR, i) for i in f_list]

#     def f(filename):
#         content = codecs.open(filename, 'r', 'utf8')
#         word_list = [line.strip() for line in content.readlines() if line.find('=====')==-1]
#         return word_list

#     words = [f(i) for i in f_list]
#     # print words[1]
#     dic = corpora.Dictionary(words)
#     corpus = [dic.doc2bow(text) for text in words]
#     print 'LDA2 TRAINING', topic_num

#     # lda模型训练
#     lda = LdaModel(corpus=corpus, id2word=dic, num_topics=topic_num)
#     data_dir = './lda2_topic_'+str(topic_num)
#     os.mkdir(data_dir)
#     data_path = os.path.join(data_dir, "jieba_lda.data")

#     lda.save(data_path)
#     for i in range(lda.num_topics-1):
#         print lda.print_topics(i)




def main():
    lda_main1()

if __name__ == '__main__':
    main()