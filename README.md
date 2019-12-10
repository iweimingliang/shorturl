# 网址转换服务

## 环境
1. python3
2. flask

## 安装(基于centos7系统)

### 安装python
```
yum install python36 -y
```

### 安装flask
```
pip3 install flask 
```

## 下载
### 安装git
git clone https://github.com/iweimingliang/shorturl.git

## 修改index.js
```
vi shorturl/templates/index.js
```
把里面的s.guanshizhai.online修改为服务器ip或者域名

## 修改配置信息
```
vim shorturl/conf.py
```
修改里面的self.key和 self.short_domain