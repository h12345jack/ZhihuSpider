#coding=utf8
import logging


from zhihuSpider.config.Config import LoggerConfig

formatter = logging.Formatter(LoggerConfig.FORMAT)

logging.basicConfig(format=LoggerConfig.FORMAT)

##
localHandler = logging.StreamHandler()
localHandler.setFormatter(formatter)
localHandler.setLevel(logging.INFO)

localLogger = logging.getLogger("consoleLogger")
localLogger.setLevel(logging.INFO)
localLogger.addHandler(localHandler)


## PIPLINE logging
piplineHandler = logging.FileHandler("pipline.log")
piplineHandler.setFormatter(formatter)
piplineHandler.setLevel(logging.INFO)

piplineLogger = logging.getLogger("piplineLogger")
piplineLogger.setLevel(logging.DEBUG)
piplineLogger.addHandler(piplineHandler)