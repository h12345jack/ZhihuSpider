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

# from gensim import corpora, models, similarities
# from gensim.models import LdaModel
# from gensim.models import TfidfModel

DATA_DIR = './cut_word_tools/answers_data'
JIEBA_DIR = './cut_word_tools/jieba_data'
JIEBA_POS_DIR = './cut_word_tools/jieba_data_pos'
TEXT_RANK_DATA = './keyword_data/text_rank'
USER_DICT = './cut_word_tools/user_dict.txt'
STOP_WORD = './cut_word_tools/stop_word.txt'

JIEBA_LDA_MODLE = './keyword_data/lda/jieba_lda.data'

QUETSION_BASED_DIR = './keyword_data/question_based'


def is_stopword(stop_word, word):
    return word in stop_word


def lda_main():
    # f_list=["100002481.txt","100003106.txt"]
    f_list = os.listdir(JIEBA_DIR)
    f_list = [os.path.join(JIEBA_DIR, i) for i in f_list]

    def f(filename):
        content = codecs.open(filename, 'r', 'utf8')
        word_list = [line.strip() for line in content.readlines()]
        return word_list

    words = [f(i) for i in f_list]
    print words[1]
    dic = corpora.Dictionary(words)
    corpus = [dic.doc2bow(text) for text in words]
    print 'LDA TRAINING'

    # lda模型训练
    lda = LdaModel(corpus=corpus, id2word=dic, num_topics=50)
    lda.save(JIEBA_LDA_MODLE)
    for i in range(lda.num_topics-1):
        print lda.print_topic(i)



'''
jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')) 直接使用，接口相同，注意默认过滤词性。
jieba.analyse.TextRank() 新建自定义 TextRank 实例
'''

def text_rank():
    '''遍历12w个文档，将结果输出来'''
    # filename="100002481.txt"
    jieba.load_userdict(USER_DICT)
    jieba.analyse.set_stop_words(STOP_WORD)
    print 'begin text_rank'
    f_list = os.listdir(DATA_DIR)
    for filename in f_list:
        f_path = os.path.join(DATA_DIR, filename)
        f = codecs.open(f_path, 'r', 'utf8')
        if not os.path.exists(os.path.join(TEXT_RANK_DATA, filename)):
            print filename, 'not exists'
        s = f.read().strip()
        rs_f = file(os.path.join(TEXT_RANK_DATA, filename), 'w')
        for x, w in jieba.analyse.textrank(s, withWeight=True, allowPOS=('ns', 'n')):
            print>> rs_f, x.encode('utf8'), ',', str(w)


def text_rank_top(topN=400):
    '''每个答案都记为1加权，遍历文档，如100002481.txt，计分求和'''
    f_list = os.listdir(TEXT_RANK_DATA)
    # f_list=["100002481.txt"]
    rs = defaultdict(float)
    for filename in f_list:
        f_path = os.path.join(TEXT_RANK_DATA, filename)
        f = codecs.open(f_path, 'r', 'utf8')
        print filename
        for line in f.readlines():
            line = line.strip()
            l_list = line.split(',')
            if len(l_list) >= 2:
                rs[l_list[0]] += float(l_list[1])
    rs2 = sorted(rs.iteritems(), key=lambda x: x[1], reverse=True)
    rs_topN = rs2[:topN]
    rs_f =file('./keyword_data/text_rank.txt','w')
    for i in rs2:
        print>>rs_f,i[0].encode("utf8")+","+str(i[1])

def test_text_rank():
    print 'begin text rank'
    text_rank()
    print 'text_rank'
    text_rank_top(400)

def test_LDA():
    print 'begin LDA models'
    lda_main()
    print 'LDA finished'


def td_idf_count1():
    '''将一个问答对视为一个文档'''
    result = file('./keyword_data/tf_idf1.txt','w')
    measurements=[]
    for i in os.listdir(JIEBA_DIR):
        i=os.path.join(JIEBA_DIR,i)
        dic=defaultdict(int)
        if i.find('.txt')!=-1 and re.search(r'[0-9]+',i):
            f=codecs.open(i,'r','utf8')
            for word in f.readlines():
                word=word.strip().encode('utf8')
                dic[word]+=1
            measurements.append(dic)
    vec = DictVectorizer()
    mat = vec.fit_transform(measurements)

    mat_name = vec.get_feature_names()
    
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(mat)

    print 'tf idf shape:', tfidf.shape
    word_tf_idf=tfidf.sum(axis=0)

    print "word_tf_idf", word_tf_idf.shape
    print "len(mat_name)", len(mat_name)
    rs=dict()
    word_tf_idf=np.array(word_tf_idf)
    print "word_tf_idf", word_tf_idf.shape

    for i,j in zip(mat_name, word_tf_idf[0,:]):
        rs[i] = j

    print "len(rs)",len(rs)
    dic2=sorted(rs.iteritems(),key=lambda x:x[1],reverse=True)
    for tmp in dic2:
            result.write(tmp[0]+','+str(tmp[1])+'\n')

def question_based():
    '''
    有一个bug，ques导出来的为数字，二ans的q_aid为字符串

    '''
    question_answer_list = dict()
    question_jl = file('./data/question/zhihu_question_clean.jl')
    for line in question_jl.readlines():
        line = line.strip()
        json_data = json.loads(line)
        q_id = str(json_data["q_id"])
        question_answer_list[q_id] = []

    print len(question_answer_list)
    answer_jl = file('./data/answers/zhihu_answer_clean.jl')
    for line in answer_jl.readlines():
        json_data = json.loads(line.strip())
        a_id = json_data["a_id"]
        a_qid = json_data["a_qid"]
        if a_id not in question_answer_list[a_qid]:
            question_answer_list[a_qid].append(a_id)

    print len(question_answer_list)
    print sum([len(question_answer_list[i]) for i in question_answer_list])

    for q_id in question_answer_list:
        rs_f = file('./keyword_data/question_based/'+str(q_id)+'.txt', 'w')
        if q_id == "19917673": 
            print question_answer_list[q_id]
        for a_id in question_answer_list[q_id]:
            i = os.path.join(JIEBA_DIR, a_id+'.txt')
            f=open(i)
            rs_f.write(f.read().strip()+'\n')
            rs_f.write("="*10+'\n')
        rs_f.close()


def question_based2():
    '''
    有一个bug，ques导出来的为数字，二ans的q_aid为字符串
    
    '''
    question_answer_list = dict()
    question_jl = file('./data/question/zhihu_question_clean.jl')
    for line in question_jl.readlines():
        line = line.strip()
        json_data = json.loads(line)
        q_id = str(json_data["q_id"])
        question_answer_list[q_id] = []

    print len(question_answer_list)
    answer_jl = file('./data/answers/zhihu_answer_clean.jl')
    for line in answer_jl.readlines():
        json_data = json.loads(line.strip())
        a_id = json_data["a_id"]
        a_qid = json_data["a_qid"]
        if a_id not in question_answer_list[a_qid]:
            question_answer_list[a_qid].append(a_id)

    print len(question_answer_list)
    print sum([len(question_answer_list[i]) for i in question_answer_list])

    for q_id in question_answer_list:
        rs_f = file('./keyword_data/question_based_pos/'+str(q_id)+'.txt', 'w')
        
        for a_id in question_answer_list[q_id]:
            i = os.path.join(JIEBA_POS_DIR, a_id+'.txt')
            f=open(i)
            rs_f.write(f.read().strip()+'\n')
            rs_f.write("="*10+'\n')
        rs_f.close()



def tf_idf_count2():
    '''
    将所有问题的回答视为一个答案
    '''
    
    result=open('./keyword_data/tf_idf2.txt','w')
    measurements=[]
    for i in os.listdir(QUETSION_BASED_DIR):
        i=os.path.join(QUETSION_BASED_DIR, i)
        dic=defaultdict(int)
        if i.find('.txt')!=-1 and re.search(r'[0-9]+',i):
            f=codecs.open(i,'r','utf8')
            for word in f.readlines():
                word=word.strip().encode('utf8')
                if word == '='*10:continue
                dic[word] += 1
            measurements.append(dic)

    vec = DictVectorizer()
    mat = vec.fit_transform(measurements).toarray()
    mat_name=vec.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(mat)
    print 'tf idf shape:', tfidf.shape

    word_tf_idf=tfidf.sum(axis=0)

    print "word_tf_idf", word_tf_idf.shape
    print "len(mat_name)", len(mat_name)
    rs=dict()
    word_tf_idf=np.array(word_tf_idf)
    print "word_tf_idf", word_tf_idf.shape

    for i,j in zip(mat_name, word_tf_idf[0,:]):
        rs[i] = j

    print "len(rs)",len(rs)
    dic2=sorted(rs.iteritems(),key=lambda x:x[1],reverse=True)
    for tmp in dic2:
            result.write(tmp[0]+','+str(tmp[1])+'\n')



def main():
    tf_idf_count2()

if __name__ == '__main__':
    main()