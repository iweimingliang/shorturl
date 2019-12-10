# 网址转换服务

## 一、环境
1. python3
2. flask

## 二、安装(基于centos7系统)

### 1.安装python
```
yum install python36 -y
```

### 2.安装flask
```
pip3 install flask 
```

### 3. 安装git
```
yum install git
```


### 4. 下载程序
```
git clone https://github.com/iweimingliang/shorturl.git
```

## 三、修改配置
## 1. 修改index.js
```
vi shorturl/templates/index.js
```
把里面的s.guanshizhai.online修改为服务器ip或者域名

## 2. 修改配置信息
```
vim shorturl/conf.py
```
修改里面的self.key和 self.short_domain


## 四、运行
### 1.测试:
```
python3 shorturl/run.py
```


### 2.正式
基于nginx和uwsgi使用

