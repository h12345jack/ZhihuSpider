#coding=utf-8

import pynlpir
import codecs
import os

from settings import DATA_DIR, JIEBA_DATA, NLPIR_DATA
from settings import USER_DICT
from settings import read_stopword
from settings import nlpir_Logger

stop_word = read_stopword()
 #设置模式为行分词模式
 #根据参数运行分词程序，从屏幕输入输出
for i in os.listdir(DATA_DIR):
    pynlpir.open()
    pynlpir.nlpir.ImportUserDict(USER_DICT)
    filename = os.path.join(DATA_DIR,i)
    f = codecs.open(filename,'r','utf8')
    content = f.read()
    filename2 = os.path.join(NLPIR_DATA,i)
    f2 = file(filename2,'w')
    try:
        seg_list = pynlpir.segment(content, pos_tagging=False)
        tmp = [w.encode("utf8") for w in seg_list if w.strip()]
        content = "\n".join([w for w in tmp if w not in stop_word])
        f2.write(content)
        print i
    except Exception as e:
        nlpir_Logger.error(e)
        nlpir_Logger.info("{} error, use jieba instead".format(i))
        with open(os.path.join(JIEBA_DATA, i)) as jieba_f:
            f2.write(jieba_f.read())
