#coding=utf-8

import jieba
import codecs
import os

from settings import DATA_DIR, JIEBA_DATA
from settings import USER_DICT
from settings import read_stopword



jieba.load_userdict(USER_DICT)
stop_word = read_stopword()

for i in os.listdir(DATA_DIR):
    filename=os.path.join(DATA_DIR,i)
    f=codecs.open(filename,'r','utf8')
    content=f.read()
    filename2=os.path.join(JIEBA_DATA,i)
    f2=file(filename2,'w')
    seg_list=jieba.cut(content.encode('utf8'),cut_all=False)
    tmp = [w.encode("utf8") for w in seg_list if w.strip()]
    content = "\n".join([w for w in tmp if w not in stop_word])
    f2.write(content)
    print i
   