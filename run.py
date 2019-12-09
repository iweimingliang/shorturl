from flask import Flask,Response,request
from flask.logging import default_handler
from flask import abort,redirect,url_for
from flask import render_template
from flask import make_response
from urllib import parse
import short_url_fun 
import token_calculation as token
import conf
import time
import json
import db
import log

config = conf.GetConfig()
app = Flask(__name__)
logwrite = log.logs()

@app.route('/urlquery',methods=['GET'])
def urlquery():
    if request.method == "GET":
        request_host_url = request.host_url
        log_content = ("action:%s Host:%s Client_ip:%s User-Agent:%s "%(request.path,request.headers.get('Host'),request.headers.get('X-Forwarded-For'),request.headers.get('User-Agent')))

        result = {}

        if not 'shorturl' in request.args.keys():
            #判断参数是否全部传递
            result['code'] = "1"
            result['errormsg'] = "shorturl parameter nof found"
            app.logger.info("%s result:%s"%(log_content,result))


            return Response(json.dumps(result,ensure_ascii=False),mimetype='application/json')

        shorturl = request.args['shorturl']

        if not short_url_fun.check_url(shorturl):
            result['code'] = "2"
            result['errormsg'] = "URL format error"
        else:
            url_list = shorturl.split('/')
            domain,shorturl_value = url_list[1],url_list[-1]

            if (domain == config.short_domain):
                result = short_url_fun.short_url_query(shorturl_value)
                if result['code'] == "0":
                    result['shorturl'] = request_host_url + result['short_url_value']
            else:
                result['code'] = "3"
                result['errormsg'] = ("Unsupported domain name. Supported domain names: %s"%(config.short_domain))

        app.logger.info("%s result:%s"%(log_content,result))

    return Response(json.dumps(result,ensure_ascii=False),mimetype='application/json')

@app.route('/urlinsert',methods=['GET','POST'])
def shorturl():
    if request.method == "POST":
    #POST请求处理
        result = {}
        request_host_url = request.host_url
        log_content = ("action:%s Host:%s Client_ip:%s User-Agent:%s "%(request.path,request.headers.get('Host'),request.headers.get('X-Forwarded-For'),request.headers.get('User-Agent')))
        #获取一些信息用来记录日志
#        print(request.data)
        url = str(request.data,encoding = "utf-8");

        if url == "":
            result['code'] = "1"
            result['errormsg'] = "URL not passed"

        elif not short_url_fun.check_url(url):
            result['code'] = "2"
            result['errormsg'] = "URL format error"

        else:
            result['source_url'] = url
#            result['source_url'] = str(url,encoding = "utf-8")
            creat_result = short_url_fun.short_url_creat(result['source_url'])
            #创建短连接

           
            if creat_result['code'] == "0":
            #创建新的短连接
                result = creat_result
                result['shorturl'] = request_host_url + result['short_url_value']
                del result['short_url_value']
            else:
            #短连接已存在，非新创建的
                result['code'] = "0"
                result['shorturl'] = request_host_url + creat_result['short_url']
                result['msg'] = "url aliready exists"

    elif request.method == "GET":
    #GET请求处理
        result = {}
        request_host_url = request.host_url
        log_content = ("action:%s Host:%s Client_ip:%s User-Agent:%s "%(request.path,request.headers.get('Host'),request.headers.get('X-Forwarded-For'),request.headers.get('User-Agent')))
        #获取一些信息用来记录日志
        #print(request.url)
        request_full_url = request.url
        url_full_path = request_full_url.split('?')
        if len(url_full_path) < 2:
            result['code'] = "1"
            result['msg'] = "URL to be shortened for delivery"
        else:
#            print(parse.unquote(url_full_path[1]))
            result['source_url'] = parse.unquote(url_full_path[1])
            creat_result = short_url_fun.short_url_creat(result['source_url'])
            #创建短连接

            if creat_result['code'] == "0":
                result = creat_result
                result['shorturl'] = request_host_url + result['short_url_value']
                del result['short_url_value']
            else:
                result['code'] = "2"
                result['shorturl'] = request_host_url + creat_result['short_url']
                result['errormsg'] = "url aliready exists"
 

    app.logger.info("%s result:%s"%(log_content,result))
    return Response(json.dumps(result,ensure_ascii=False),mimetype='application/json')

@app.route('/md5',methods=['GET','POST'])
def md5():
    result = {}

    log_content = ("action:%s Host:%s Client_ip:%s User-Agent:%s "%(request.path,request.headers.get('Host'),request.headers.get('X-Forwarded-For'),request.headers.get('User-Agent')))
    if request.method == "POST":
        if 'content' in request.form.keys():
            result['request_content'] = request.form['content']
            result['token_value'] = token.calculation_md5(request.form['content'])
            result['code'] = 0
        else:
            result['errormsg'] = "Content parameter not passed"
            result['code'] = 1

    elif request.method == "GET":
#        app.logger.info("InfoTest")
#        logwrite.info("test")
        if 'content' in request.args.keys():
            result['request_content'] = request.args['content']
            result['token_value'] = token.calculation_md5(request.args['content'])
            result['code'] = 0
        else:
            result['errormsg'] = "Content parameter not passed"
            result['code'] = 2

    else: 
        result['errormsg'] = "Unsupported http method"
        result['code'] = 3

    app.logger.info("%s result:%s"%(log_content,result))

    return Response(json.dumps(result,ensure_ascii=False),mimetype='application/json')

@app.route('/<username>',methods=['GET'])
def short_get(username):
    if request.method == "GET":
        log_content = ("action:%s Host:%s Client_ip:%s User-Agent:%s "%(request.path,request.headers.get('Host'),request.headers.get('X-Forwarded-For'),request.headers.get('User-Agent')))

        shorturl = request.base_url
        short_url_value = shorturl.split('/')[-1]
        result = short_url_fun.short_url_query(short_url_value)
        if result['code'] == "1":
            result['source_url'] = shorturl
        else:
            app.logger.info("%s result:%s"%(log_content,result))
            return redirect(result['originalurl'])
            
        app.logger.info("%s result:%s"%(log_content,result))

    return Response(json.dumps(result,ensure_ascii=False),mimetype='application/json')

@app.route('/index.html',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/favicon.ico',methods=['GET'])
def faviceon():
    return Response('img/favicon.ico',mimetype="image/png")


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'),404)
#    resp.headers['X-Somethind'] = 'A value'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')
