#coding=utf8

## 数据文件夹
import os
import sys


##
#
#
TOPIC_ID_LIST = [
    "19551771",
    "19560960",
    "19771791",
    "19560329",
    "19693641",
    "19866333",
    "19966764",
    "19886917",
    "20028839",
    "19640444",
    "19568014",
    "19670327",
    "19564157",
    "19572310",
    "19674269",
    "19679280",
    "19737971",
    "20073497",
    "19817792",
    "19571159",
    "19558839",
    "20071997",
    "20065323",
    "19863120",
    "19631981",
    "19584046",
    "20073497",
    "19552079",
    "19591321",
    "19630026",
    "19619615",
    "19760061",
    "19673221",
    "19591867",
    "19591490",
    "19846288",
    "19628357",
    "19900873",
    "19666541",
    "19562469",
    "19565614",
    "19719894",
    "19728176",
    "19570405",
    "19649098",
    "19610790",
    "19926142",
    "19837670",
    "20005320"
]



##
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
  os.mkdir(DATA_DIR)

## 数据库配置


## 日志配置

class LoggerConfig():
    LOG_PATH_CRAWLER = './data/logs/crawler.log'
    FORMAT = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'


## requests 相关配置

### Common
#
#
#
#### URL
URL = {
  "HOMEPAGE": "https://www.zhihu.com",
  "LOGIN": "https://www.zhihu.com/login/email",
  "QUESTIONS": "https://www.zhihu.com/log/questions",
  "QUESTION_PREFIX": "https://www.zhihu.com"
}
  
### TIMEOUT
TIMEOUT = 10

########## authorization重要
HEADERS={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.",
    "X-Requested-With": "XMLHttpRequest",
    "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
}

### Login

XSRF_PATH = './config/data/_xsrf.data'
COOKIES_PATH = './config/data/cookies.data'

COOKIES_RAW_PATH = './config/data/cookies_raw.data'
if not os.path.exists(COOKIES_RAW_PATH):
  print("cookie raw not exists, pls add it")
  sys.exit(-1)


USER_DICT = {
    'huang-ting-ting-ti-zu-qiu':'huang-ting-ting-ti-zu-qiu',
    'jackhuang':'jackhuang',
    'default':'cookies'
}



### 
RECOMMENDATIONS_URL = 'https://www.zhihu.com/api/v4/explore/recommendations?include=data%5B*%5D.answer.voteup_count%3Bdata%5B*%5D.article.voteup_count'

INCLUDE = 'data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics'