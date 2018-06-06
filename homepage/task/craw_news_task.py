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
    iron_log.info('start to craw...')
    for i in range(3):
        iron_log.info('start to craw... ' + str(i))
        craw()
        iron_log.info('end crawing. ' + str(i))
    iron_log.info('end crawing.')


def delete_news():
    iron_log.info('start to delete_news')
    start_time = datetime.datetime.now() + datetime.timedelta(hours=-3)
    result = CrawNews.objects.filter(create_time__lt=start_time).delete()
    iron_log.info(str(result[0]) + ' objects deleted.')


def craw():
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    print "cookie:", cookie
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    # 此处的open方法同urllib2的urlopen方法，也可以传入request
    response = opener.open('https://www.csdn.net/api/articles?type=more&category=home')

    res_str = response.read()
    res_obj = json.loads(res_str, encoding='utf-8')
    articles = res_obj.get('articles')
    iron_log.info(str(len(articles)) + ' results got.')
    for article in articles:
        title = article.get('title')
        content = article.get('summary')
        pub_date = article.get('created_at')
        url = article.get('url')
        author = article.get('nickname')
        iron_log.info('title:' + title)
        # iron_log.info('content:' + content)
        iron_log.info('pub_date:' + pub_date)
        iron_log.info('url:' + url)
        iron_log.info('author:' + author)
        craw_new = CrawNews(title=title, content=content, pub_date=pub_date,
                            url=url, author=author, origin_site=CrawNews.CSDN)
        craw_new.save()
        iron_log.info('saved')
