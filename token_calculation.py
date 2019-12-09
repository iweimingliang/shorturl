import time
import hashlib
import logging


def get_timestamp():
    timestamp = str(time.time() * 1000)
#    print(timestamp)
    return timestamp.split('.')[0]


def calculation_md5(content):
    content_md5 = hashlib.md5()
    content_md5.update(content.encode())
    return content_md5.hexdigest()



