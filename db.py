import conf
import sqlite3


def shorturl_query(shorturl_value):
    result = {}
    config = conf.GetConfig()

    sqlite_db_conn = sqlite3.connect(config.db_conf_path)
    sqlite_db_cu = sqlite_db_conn.cursor()
#    url_md5 = token_ca.calculation_md5(url)
    query_sql = (("SELECT id, originalurl, md5value, shorturl  from url where shorturl='%s'")%shorturl_value)
#    query_sql = "SELECT id, originalurl, md5value, shorturl  from url where md5value=\'" + url_md5 + "\'"

    cursor = sqlite_db_cu.execute(query_sql)
    data = cursor.fetchone()

    if not data:
        result['code'] = "1"
        result['msg'] = "Url does not exist"
    else:
        result['code'] = "0"
        result['id'] = data[0]
        result['originalurl'] = data[1]
        result['md5value'] = data[2]
        result['short_url_value'] = data[3]

    sqlite_db_conn.close()

    return result


def data_query(url,url_md5):
    result = {}
    config = conf.GetConfig()

    sqlite_db_conn = sqlite3.connect(config.db_conf_path)
    sqlite_db_cu = sqlite_db_conn.cursor()
#    url_md5 = token_ca.calculation_md5(url)
    query_sql = (("SELECT id, originalurl, md5value, shorturl  from url where md5value='%s'")%url_md5)
#    query_sql = "SELECT id, originalurl, md5value, shorturl  from url where md5value=\'" + url_md5 + "\'"

    cursor = sqlite_db_cu.execute(query_sql)
    data = cursor.fetchone()

    if not data:
        result['code'] = "0"
        result['msg'] = "Url does not exist"
    else:
        result['code'] = "1"
        result['msg'] = "Url already exists"
        result['id'] = data[0]
        result['suorce_url'] = data[1]
        result['md5_value'] = data[2]
        result['short_url'] = data[3]

    sqlite_db_conn.close()

    return result

def query_sum():
    config = conf.GetConfig()

    sqlite_db_conn = sqlite3.connect(config.db_conf_path)
    sqlite_db_cu = sqlite_db_conn.cursor()

    query_sql = "SELECT COUNT(*) FROM URL"

    cursor = sqlite_db_cu.execute(query_sql)
    data = cursor.fetchone()

    sum = data[0]   
    
    return sum

def data_insert(url,url_md5,shorturl_value):
    result = {}
    config = conf.GetConfig()

    sqlite_db_conn = sqlite3.connect(config.db_conf_path)
    sqlite_db_cu = sqlite_db_conn.cursor()

    insert_sql = "INSERT INTO URL (ORIGINALURL, MD5VALUE, SHORTURL) VALUES ('%s', '%s', '%s')"%(url,url_md5,shorturl_value)

    cursor = sqlite_db_cu.execute(insert_sql) 

    sqlite_db_conn.commit()
    sqlite_db_conn.close()

    result['code'] = "0"
#    result['md5'] = url_md5
#    result['shorturl_value'] = shorturl_value

    return result

def main():
    url = 'https://www.guanshizhai.onlien/12'
    result = data_query(url)
    if result['code'] == "0":
        print("url does not exist")
    elif result['code'] == "1": 
#        result['msg'] = "Url already exists"
        print("Url already exists")

    result = data_insert(url)
    if result['code'] == "0":
        print("ok")
    elif result['code'] == "1": 
        result['msg'] = "Url already exists"
        print("Url already exists")

    print(query_sum())

if __name__ == '__main__':
    main()