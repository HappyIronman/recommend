# -*- coding: utf-8 -*-
import datetime


def default_cal_weight_func(item):
    interval = (datetime.datetime.now() - item.create_time.replace(tzinfo=None)).seconds
    return 1 + 1.0 / (interval + 20)


def like_log_cal_weight_func(like_log):
    interval = (datetime.datetime.now() - like_log.create_time.replace(tzinfo=None)).seconds
    val = 1 + 1.0 / (interval * 3 + 30)
    if like_log.is_like:
        return val
    return -1 * val
