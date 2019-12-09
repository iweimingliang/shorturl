import os
import sys
import logging
import conf


class logs():
    def __init__(self):
        #日志路径和格式配置
        config = conf.GetConfig()
        self.log_path = config.log_path
        logging.basicConfig(level=logging.INFO,
#            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            format='%(asctime)s %(filename)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.log_path,
            filemode='a'
        )

    def info(self,content):
        logging.info(content)

    def error(self,content):
        logging.error(content)