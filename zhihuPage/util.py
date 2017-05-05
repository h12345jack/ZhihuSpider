#coding=utf8
import os
import random
import time

from config.Config import DATA_DIR
from config.Config import NEED_CRAWL_URL_FILE

def read_data():
    '''
    get url to crawl
    '''
    file_list = [i for i in os.listdir(DATA_DIR)]
    url_list = set()
    for f_path in file_list:
        with open(os.path.join(DATA_DIR,f_path)) as f:
            for line in f.readlines():
                url_list.add(line.strip())
    with open(NEED_CRAWL_URL_FILE,'w') as f:
        for i in url_list:
            f.write(i+'\n')

def time_sleep_random(a,b):
    '''
    随机休息a-b之间的随机数
    '''
    time.sleep(random.randint(a,b))


def main():
    read_data()

if __name__ == '__main__':
    main()
