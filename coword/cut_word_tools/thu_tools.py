#coding=utf-8

import thulac
import codecs
import os
from settings import DATA_DIR, JIEBA_DATA , THU_DATA
from settings import USER_DICT
from settings import read_stopword

thu1 = thulac.thulac("-seg_only")
stop_word = read_stopword()
 #设置模式为行分词模式
 #根据参数运行分词程序，从屏幕输入输出
for i in os.listdir(DATA_DIR):
    filename = os.path.join(DATA_DIR,i)
    f=codecs.open(filename,'r','utf8')
    content = f.read()
    filename2 = os.path.join(THU_DATA,i)
    f2 = file(filename2,'w')
    log = file("thu_tool.log", 'a')
    try:
        seg_list = thu1.cut(content.encode('utf8'))
        tmp = [w for w in seg_list if w.strip()]
        content = "\n".join([w for w in tmp if w not in stop_word])
        f2.write(content)
        print i
    except Exception as e:
        print>>log, i, e
        print i, 'use jieba instead'
        with open(os.path.join(JIEBA_DATA, i)) as jieba_f:
            f2.write(jieba_f.read())