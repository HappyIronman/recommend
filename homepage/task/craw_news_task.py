# -*- coding: utf-8 -*-
import cookielib
import json
import logging
import urllib2

# 声明一个CookieJar对象实例来保存cookie
import datetime

from homepage.models import CrawNews

iron_log = logging.getLogger('ironman')

cookie = cookielib.CookieJar()


def offline_craw():
    # 删除原有数据
    # CrawNews.objects.all().delete()
    print ('start to craw...')
    for i in range(3):
        print ('start to craw... ' + str(i))
        craw()
        print ('end crawing. ' + str(i))
    print ('end crawing.')


def delete_news():
    print ('start to delete_news')
    start_time = datetime.datetime.now() + datetime.timedelta(hours=-3)
    result = CrawNews.objects.filter(create_time__lt=start_time).delete()
    print (str(result[0]) + ' objects deleted.')


def craw():
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    # 此处的open方法同urllib2的urlopen方法，也可以传入request
    response = opener.open('https://www.csdn.net/api/articles?type=more&category=home')

    res_str = response.read()
    res_obj = json.loads(res_str, encoding='utf-8')
    articles = res_obj.get('articles')
    print (str(len(articles)) + ' results got.')
    print articles
    for article in articles:
        title = article.get('title')
        content = article.get('summary')
        pub_date = article.get('created_at')
        url = article.get('url')
        author = article.get('nickname')
        print ('title:' + title)
        # print ('content:' + content)
        print ('pub_date:' + pub_date)
        print ('url:' + url)
        print ('author:' + author)
        craw_new = CrawNews(title=title, content=content, pub_date=pub_date,
                            url=url, author=author, origin_site=CrawNews.CSDN)
        craw_new.save()
        print ('saved')
