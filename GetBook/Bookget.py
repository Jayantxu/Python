from urllib.request import urlopen
from bs4 import BeautifulSoup,Comment
import urllib
import re
import datetime
import random
import pymysql
import os


conn = pymysql.connect(host='127.0.0.1',user=' ',passwd='',db='mysql',charset='utf8')
cur = conn.cursor()
cur.execute("USE pythondb")

#存储数据
def store(title,author,belongg,leibie,sum,PicUrl):
    cur.execute("INSERT INTO PythonBook (title,author,belongg,leibie,summaryy,PicUrl) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")", (title,author,belongg,leibie,sum,PicUrl))
    cur.connection.commit()

#网址
##html = urlopen("http://www.dqiu.net/books/p/1.html")

##bsObj = BeautifulSoup(html,"html.parser")

# 因为是分页的，存储每一页的url先？~
##href_ = bsObj.find('div', id="pagenate").find_all("a")
##tags = []
# 然后转换并补全路径；此处只选择爬
##for each in href_:
##    each = each.get('href')
##    href_ = "http://www.dqiu.net"
##    url = href_ + str(each)
# 获取写入文件的链接

#打开文本文件里的网址，选择性读取
with open('testUrl.txt') as file:
    for url in file:
    # 打开每一页
        html = urlopen(url)
        bsObj = BeautifulSoup(html, "html.parser")
        #选出所有的media的div
        bsss = bsObj.find_all('div',class_='media')
        for tag in bsss:
            #书名
            title = tag.find('h4',class_='media-heading').find('a').text
            #抓取图片，并保存至文件系统---同时补全不同的路径，可放入数据库
            Pic = tag.find('img',class_='media-object')['src']
            #清洗图片来源路径
            if Pic.startswith('http') :
                pic = Pic
            else:
                pic = "http://www.dqiu.net"+Pic
            #所有p标签的信息
            infomation = tag.find('div',class_='media-body').find_all('p')
            #只要前四个，因为有一个评论，没用的
            #作者**-数据清洗一下
            author = infomation[0].text
            author2 = author.replace('作者','')
            #清洗出版信息
            belong = infomation[1].text
            belong2 = belong.replace('出版信息','')
            #清洗类别
            leibie = infomation[3].text
            leibie2 = leibie.replace('类别','')
            #清洗摘要
            ######清洗数据的问题
            infoo = tag.find('div',class_='media-body').findAll(text=lambda text:isinstance(text, Comment))
            infoo2 = str(infoo)
            infoo3 = infoo2.replace("<h5>摘要</h5>\\r\\n","").replace("<p>","").replace("</p>\\r\\n","").replace("['","").replace("]","").replace("'","")
            #保存图片至本地文件系统,并给出路径，数据库保存用
            urllib.request.urlretrieve(pic,'F:\Python项目\BookShopPic\%s.jpg' %title)
            strr = 'F:\Python项目\BookShopPic\%s.jpg' %title
            #转存数据库的方法
            store(title,author2,belong2,leibie2,infoo3,strr)
        print("---读完 一 页---")
print("---结束---")
