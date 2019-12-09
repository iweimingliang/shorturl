import db
import re
import token_calculation as token_ca



def short_url_creat(url):
    url_md5 = token_ca.calculation_md5(url)
    query_result = db.data_query(url,url_md5)

    if query_result['code'] == "0":
        line = hex(db.query_sum() + 1)

        shorturl_value = str(line)

        creat_result = db.data_insert(url,url_md5,shorturl_value)

        creat_result['msg'] = "Short URL created successfully"
        creat_result['source_url'] =  url
        creat_result['source_url_md5'] =  url_md5
        creat_result['short_url_value'] = shorturl_value 

        return creat_result

    elif query_result['code'] == "1": 
        return query_result

def short_url_query(shorturl_value):
    query_result = db.shorturl_query(shorturl_value)
    return query_result


def check_url(url):
#    re_url = re.compile(r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    re_url = re.compile(r'(http[s]?:\/\/).*')
#    re_url = re.compile(r'http://(\d+\.\d+\.\d+\.\d+:\d+)/.*\.apk')
    url_check_result = re_url.match(url)
    if url_check_result:
        return True
    else:
        return False