# -*- coding: utf-8 -*-
import math

from homepage.models import Recommend_Result

USER_STRATEGY_DIC = {}

HOT_STRATEGY = 'HOT_STRATEGY'
MILD_STRATEGY = 'MILD_STRATEGY'
COLD_STRATEGY = 'COLD_STRATEGY'


def get_strategy(user_id, page, size):
    count = USER_STRATEGY_DIC.get(user_id)
    if not count:
        count = Recommend_Result.objects.filter(user_id=user_id).count()
        print count
        USER_STRATEGY_DIC[user_id] = count

    if count >= 10:
        print 'hot_strategy'
        return hot_strategy(page, size)
    elif 5 <= count < 10:
        print 'mild_strategy'
        return mild_strategy(page, size)
    else:
        print 'cold_strategy'
        return cold_strategy(page, size, count)


def hot_strategy(page, size):
    return int((size - 3) / 2 * math.log10(page + 9) + 3)


def mild_strategy(page, size):
    return int((size - 3) / 2 * math.log10(page + 9) + 2)


def cold_strategy(page, size, count):
    if count == 0 or page >= count:
        return 0
    return 1
