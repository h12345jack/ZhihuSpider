#coding=utf8
import codecs
import logging

DATA_DIR = './answers_data'

JIEBA_DATA = './jieba_data'

JIEBA_DATA_POS = './jieba_data_pos'

NLPIR_DATA = './nlpir_data'

THU_DATA = './thu_data'

USER_DICT = './user_dict.txt'

STOP_WORD = './stop_word.txt'


def read_stopword():
    '''
    读取停用词，返回一个集合
    '''
    stopword=set()
    f=codecs.open(STOP_WORD,'r','utf8')
    for i in f.readlines():
        if i.strip():
            stopword.add(i.strip().encode('utf8'))
    return stopword


class LoggerConfig():
    FORMAT = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'

formatter = logging.Formatter(LoggerConfig.FORMAT)
logging.basicConfig(format=LoggerConfig.FORMAT)


thu_Handler = logging.FileHandler("thu_tools.log")
thu_Handler.setFormatter(formatter)
thu_Handler.setLevel(logging.INFO)

thu_Logger = logging.getLogger("thu_Handler")
thu_Logger.setLevel(logging.DEBUG)
thu_Logger.addHandler(thu_Handler)


nlpir_Handler = logging.FileHandler("nlpir_tools.log")
nlpir_Handler.setFormatter(formatter)
nlpir_Handler.setLevel(logging.INFO)

nlpir_Logger = logging.getLogger("nlpir_Handler")
nlpir_Logger.setLevel(logging.DEBUG)
nlpir_Logger.addHandler(nlpir_Handler)