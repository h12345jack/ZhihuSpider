# -*- coding: utf-8 -*-

# Scrapy settings for zhihuSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
import logging


BOT_NAME = 'zhihuSpider'

SPIDER_MODULES = ['zhihuSpider.spiders']
NEWSPIDER_MODULE = 'zhihuSpider.spiders'

LOG_FILE = 'zhihu.log'
LOG_LEVEL= 'INFO'
LOG_ENCODING=None

COOKIES_DEBUG = False
RETRY_ENABLED = True
REDIRECT_ENABLED = True

DEPTH_LIMIT=0
DEPTH_PRIORITY=0

CONCURRENT_ITEMS = 1000
CONCURRENT_REQUESTS = 100
#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 200
CONCURRENT_REQUESTS_PER_SPIDER=100

DNSCACHE_ENABLED = True

DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 10

ITEM_PIPELINES = {  
    # 'zhihuSpider.pipelines.JsonWriterPipline': 300,
    'zhihuSpider.pipelines.DataValidatePipline': 200,
    'zhihuSpider.pipelines.MySQLWritePipline': 300
}

DOWNLOADER_MIDDLEWARES = {
    # 'zhihuSpider.misc.middleware.CustomHttpProxyMiddleware': 80,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':80,
    'zhihuSpider.misc.middleware.CustomUserAgentMiddleware': 81
}


HEADER={
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

COOKIES_ENABLED=True

DATA_STORE_DIR = './data_storge'
if not os.path.exists(DATA_STORE_DIR):
    os.mkdir(DATA_STORE_DIR) 

NEED_CRAWL_URL_FILE = './config/need_crawl_url.txt'





MYSQL_URI = "mysql://root:admin@localhost:3306/zhihu_may?charset=utf8"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuSpider (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Host": "www.zhihu.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
    "Referer": "http://www.zhihu.com/people/jackhuang",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuSpider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihuSpider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'zhihuSpider.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'


### my config


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

QUESTION_COMMENT = 'https://www.zhihu.com/api/v4/questions/57868057/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=10&offset=0&status=open'