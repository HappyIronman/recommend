# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import decimal
import json
import logging

from django.core import serializers
from django.db.models import QuerySet, Model
from django.http import HttpResponse, JsonResponse

# Create your views here.
from homepage import constants
from homepage.engine import processor
from homepage.models import User

iron_log = logging.getLogger('ironman')


def test1(request):
    return HttpResponse('hahaha')


def get_recommend_homepage(request):
    # 1.认证
    partner_id = request.POST.get('partnerId', '')
    user_unique_id = request.POST.get('userId', '')
    page = int(request.POST.get('page', 0))
    size = int(request.POST.get('size', 5))
    iron_log.info('A new Request GOT:')
    iron_log.info('partnerId:' + str(partner_id))
    iron_log.info('userId:' + str(user_unique_id))
    iron_log.info('page:' + str(page))
    iron_log.info('size:' + str(size))
    if not verify(partner_id):
        return JsonResponse(ResponseEntity(False, 2001, '认证失败'), safe=False,
                            json_dumps_params={'default': custom_serializer})
    if user_unique_id == '':
        return JsonResponse(ResponseEntity(False, 3001, 'userId不能为空'), safe=False,
                            json_dumps_params={'default': custom_serializer})

    # 2.获取推荐列表
    user_id = User.objects.using('forum').get(unique_id=user_unique_id).id
    recommend_list = processor.process(user_id, page, size)

    # news_set = CrawNews.objects.filter(create_time=datetime.date.today())[page * size:(page + 1) * size]
    # 3.组装返回
    return JsonResponse(ResponseEntity(True, 1000, recommend_list), safe=False,
                        json_dumps_params={'default': custom_serializer})


def verify(partner_id):
    return partner_id in constants.PARTNER_ID_SET


def custom_serializer(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, ResponseEntity):
        return {'success': obj.get_success, 'code': obj.get_code, 'msg': obj.get_msg}
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    elif isinstance(obj, QuerySet):
        return json.loads(serializers.serialize("json", obj))
    elif isinstance(obj, Model):
        return json.loads(serializers.serialize('json', [obj])[1:-1])
    print type(obj)
    raise TypeError('%r is not JSON serializable' % obj)


class ResponseEntity(object):
    def __init__(self, success, code, msg):
        self.__success = success
        self.__code = code
        self.__msg = msg

    def set_success(self, success):
        self.__success = success

    def set_code(self, code):
        self.__code = code

    def set_msg(self, msg):
        self.__msg = msg

    @property
    def get_success(self):
        return self.__success

    @property
    def get_code(self):
        return self.__code

    @property
    def get_msg(self):
        return self.__msg
