# -*- coding: utf-8 -*-
from homepage.engine.weight_func import default_cal_weight_func, like_log_cal_weight_func
from homepage.models import *

IS_READY = False
# 系统常量，不可任意更改
VIEW_LOG = 'view_log'
LIKE_LOG = 'like_log'
COMMENT_LOG = 'comment_log'

ORIGIN_MODEL = 'origin_model'
MOVE_MODEL = 'move_model'
REL_MODEL = 'rel_model'
WEIGHT_FUNC = 'weight_func'

LOG_MODEL_DIC = {
    VIEW_LOG: {ORIGIN_MODEL: View_Log, MOVE_MODEL: Move_View, REL_MODEL: Rel_View,
               WEIGHT_FUNC: default_cal_weight_func},
    LIKE_LOG: {ORIGIN_MODEL: Like_Log, MOVE_MODEL: Move_Like, REL_MODEL: Rel_Like,
               WEIGHT_FUNC: like_log_cal_weight_func},
    COMMENT_LOG: {ORIGIN_MODEL: Comment, MOVE_MODEL: Move_Comment, REL_MODEL: Rel_Comment,
                  WEIGHT_FUNC: default_cal_weight_func}
}

PARTNER_ID_SET = set()

# 自定义参数如下，可调整
VIEW_WEIGHT = 2.0
LIKE_WEIGHT = 5.0
COMMENT_WEIGHT = 8.0

PARTNER_IDS = 'superheroironman;superherothor'
