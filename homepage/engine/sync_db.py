# -*- coding: utf-8 -*-
import logging

from homepage.constants import *

iron_log = logging.getLogger('ironman')


def sync_log(log_type):
    model_dict = LOG_MODEL_DIC.get(log_type)
    iron_log.info('start to sync_' + log_type + '...')
    try:
        sync_each_table(model_dict.get(ORIGIN_MODEL), model_dict.get(MOVE_MODEL), model_dict.get(WEIGHT_FUNC))
    except Exception, ex:
        iron_log.exception(ex)
    iron_log.info('end sync_' + log_type + '.')


def sync_each_table(origin_model, target_model, cal_weight_func=default_cal_weight_func):
    page = 0
    size = 100
    # 删除已有数据
    target_model.objects.all().delete()

    # 分页获取view_log
    view_log_list = get_log_list(origin_model, page, size)

    while len(view_log_list) != 0:
        for view_log in view_log_list:
            try:
                try:
                    rel_view = target_model.objects.get(user_id=view_log.user_id, blog_id=get_target_id(view_log))
                    rel_view.weight = rel_view.weight + cal_weight_func(view_log)
                    rel_view.save()
                    # iron_log.info('updated..'
                except target_model.DoesNotExist:
                    rel_view = target_model(user_id=view_log.user_id, blog_id=get_target_id(view_log),
                                            weight=cal_weight_func(view_log))
                    rel_view.save()
                    # iron_log.info('created..'
            except Exception, ex:
                iron_log.exception(ex)
        page += 1

        view_log_list = get_log_list(origin_model, page, size)


def get_log_list(origin_model, page, size):
    if hasattr(origin_model, 'disabled'):
        view_log_list = list(
            origin_model.objects.using('forum').filter(type=2, disabled=False)[page * size: (page + 1) * size])
    else:
        view_log_list = list(
            origin_model.objects.using('forum').filter(type=2, deleted=False)[page * size: (page + 1) * size])
    return view_log_list


def get_target_id(log):
    if hasattr(log, 'target_id'):
        target_id = log.target_id
    else:
        target_id = log.reply_id
    return target_id
