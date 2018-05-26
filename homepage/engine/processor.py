# -*- coding: utf-8 -*-
import logging
import re

from homepage.filter import result_filter
from homepage.models import Recommend_Result, CrawNews, Blog, User

iron_log = logging.getLogger('ironman')


def process(user_id, page, size):
    local_num = result_filter.get_strategy(user_id, page, size)
    start_index = 0
    for i in range(page):
        start_index += result_filter.get_strategy(user_id, i, size)
    local_recommend_set = Recommend_Result.objects.filter(user_id=user_id).order_by('weight')[
                          start_index:start_index + local_num]
    external_num = size - local_num
    external_recommend_set = set()
    if external_num > 0:
        external_recommend_set = CrawNews.objects.order_by('-create_time')[
                                 page * external_num:(page + 1) * external_num]

    recommend_list = []

    for external_item in external_recommend_set:
        recommend_item_vo = RecommendItemVO(type=RecommendItemVO.TYPE_EXTERNAL, url=external_item.url,
                                            title=external_item.title, author=external_item.author, author_id=None,
                                            content=external_item.content, pub_date=external_item.pub_date,
                                            origin_site=external_item.origin_site, blog_id=None, weight=None)
        recommend_list.append(recommend_item_vo.__dict__)

    for local_item in local_recommend_set:
        blog_id = local_item.blog_id
        weight = local_item.weight
        try:
            blog = Blog.objects.using('forum').get(id=blog_id)
            user = User.objects.using('forum').get(id=blog.user_id)
            short_content = cut_content(blog.content)
            recommend_item_vo = RecommendItemVO(type=RecommendItemVO.TYPE_LOCAL, blog_id=blog.unique_id, url=None,
                                                title=blog.title, author=user.username, author_id=user.unique_id,
                                                content=short_content,
                                                pub_date=blog.create_time, weight=weight)
            recommend_list.append(recommend_item_vo.__dict__)
        except Blog.DoesNotExist, ex:
            iron_log.exception(ex)
            iron_log.error('Exception, processor will continue.')
    iron_log.info(recommend_list)
    return recommend_list


def cut_content(content):
    res = ''
    if not content:
        return res
    dr = re.compile(r'<[^>]+>', re.S)
    res = dr.sub('', content)
    return res[0:150]


class RecommendItemVO(object):
    TYPE_LOCAL = 'LOCAL'
    TYPE_EXTERNAL = 'EXTERNAL'

    def __init__(self, type, blog_id, url, title, author, author_id, content, pub_date, weight, origin_site='LOCAL'):
        self.type = type
        self.blog_id = blog_id
        self.url = url
        self.title = title
        self.author = author
        self.author_id = author_id
        self.content = content
        self.pub_date = pub_date
        self.weight = weight
        self.origin_site = origin_site
