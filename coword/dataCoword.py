#coding=utf8

import os
import codecs

RS_KEYWORD_DATA = './'
JIEBA_DIR = ''

def getDictionary(filename):
    '''获取词典'''
    pass



def _get_filedic(filename):
    dic=dict()
    f=codecs.open(filename,'r','utf8')
    for i in f.readlines():
        i=i.strip().encode('utf8').split(' ')
        if i[0]=='==========':continue
        word=i[0]
        if len(word)<1 :continue
        if word in dic:
            dic[word]+=1
        else:
            dic[word]=1
    return dic


def _get_filedic2(filename):
    dic_return=[]
    dic=dict()
    f=codecs.open(filename,'r','utf8')
    for i in f.readlines():
        i=i.strip().encode('utf8').split(' ')
        if i[0]=='==========':
            dic_return.append(dic)
            dic=dict()
            continue
        word=i[0]
        if len(word)<1 :continue
        if word in dic:
            dic[word]+=1
        else:
            dic[word]=1
    return dic_return

def getCooccur2(j1, j2, file_dic_list):
    data=0
    for file_dic in file_dic_list:
        j1_v1=0
        j2_v1=0
        if j1 in file_dic:
            j1_v1 += file_dic[j1]
        if j2 in file_dic:
            j2_v1 += file_dic[j2]
        data += j1_v1 if j1_v1 < j2_v1 else j2_v1
    return data


def getMatrix():
    data_file = RS_KEYWORD_DATA
    dic = list(getDictionary(data_file))
    print len(dic)

    mat = dict()
    question_dir = JIEBA_DIR
    for filename in os.listdir(question_dir):
        filename = os.path.join(question_dir, filename)
        for j1 in dic:
            for j2 in dic:
                if j1 not in mat:
                    mat[j1] = dict()
                if j2 not in mat[j1]:
                    mat[j1][j2] = 0
                else:
                    mat[j1][j2] += getCooccur2(j1, j2, )

