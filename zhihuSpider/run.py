#coding=utf8
from scrapy import cmdline
'''
将need_spider中的部分进行多线程抓取
为了更好的实现任务的并发，将共享的资源分离抓取

'''
need_spider=[
"19551771",
"19552079"
# "19673221",
# "19591867",
# "19760061",
# "19630026",
# "19591321",
# "19619615",
# "19591490",
# "19846288",
# "19666541",
# "19771791",
# "19560329",
# "19568014",
# "19886917",
# "19866333",
# "19693641",
# "20028839",
# "19670327",
# "19564157"

# "19640444",
# "19966764",
# "19562469",
# "19649098",
# "19565614",
# "19728176",
# "19719894",
# "19610790",
# "19570405",
# "19560960",
# "19572310",
# "19674269",
# "19679280",
# "19571159",
# "19558839",
# "19817792",
# "19737971",
# "19926142",
# "19900873",
# "19837670",
# "20005320",
# "19628357"
]

import os


def work_it(i):
    os.system(i)

def main():
    import multiprocessing 
    from multiprocessing import Pool
    multiprocessing.freeze_support()
    record=[]
    cmd_list=[]
    pool = Pool(processes=2) 
    for i in need_spider:
        cmd_str="scrapy crawl zhihu_topic -o {}.json -t jsonlines -a filename={}.txt --logfile {}.log".format(i,i,i)
        cmd_list.append(cmd_str)
    for i in cmd_list:
        result = pool.apply_async(work_it, (i,))

    pool.close()
    pool.join()
        

if __name__ == '__main__':
    main()