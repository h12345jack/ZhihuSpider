#coding=utf8
import logging.config
import logging


# classifyHandler = TimedRotatingFileHandler(LoggerConfig.LOG_PATH_CLASSIFY, when='d', interval=1)
classifyHandler = logging.StreamHandler()
classifyHandler.setLevel(logging.DEBUG)
classifyHandler.setFormatter(formatter)

classifyLogger = logging.getLogger("classifyLogger")
classifyLogger.setLevel(logging.DEBUG)
classifyLogger.addHandler(classifyHandler)