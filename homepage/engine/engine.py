# -*- coding: utf-8 -*-
import logging

from homepage.constants import LOG_MODEL_DIC, LIKE_LOG, VIEW_LOG, COMMENT_LOG, VIEW_WEIGHT, LIKE_WEIGHT, COMMENT_WEIGHT, \
    REL_MODEL, MOVE_MODEL
from homepage.engine import user_cf, sync_db
from homepage.models import Blog, Recommend_Result

iron_log = logging.getLogger('ironman')


def offline_cal_recommend_list():
    cal_rel_list(VIEW_LOG)
    cal_rel_list(LIKE_LOG)
    cal_rel_list(COMMENT_LOG)
    # 计算推荐列表并落库
    cal_recommend_list_and_save()


def cal_rel_list(log_type):
    try:
        # 1.同步db
        sync_db.sync_log(log_type)
        # 2.应用算法计算离线相关表并落库
        apply_algorithm_and_save(log_type)
    except Exception, ex:
        iron_log.exception(ex)


def cal_recommend_list_and_save():
    iron_log.info('start to cal_recommend_list...')
    try:
        # 1.加权计算Rel_View, Rel_Like, Rel_Comment三张表合并后的原始推荐列表
        rel_view_dic = assemble_rel_dic_from_db(VIEW_LOG)
        rel_like_dic = assemble_rel_dic_from_db(LIKE_LOG)
        rel_comment_dic = assemble_rel_dic_from_db(COMMENT_LOG)
        # 1.1 先求userId并集作为key
        recommend_dic = {}
        user_id_set = set(rel_view_dic.keys()) | set(rel_like_dic.keys()) | set(rel_comment_dic.keys())
        for user_id in user_id_set:
            recommend_dic[user_id] = {}
            blog_id_set = set(rel_view_dic.get(user_id).keys() if rel_view_dic.get(user_id) else []) | set(
                rel_like_dic.get(user_id).keys() if rel_like_dic.get(user_id) else []) | set(
                rel_comment_dic.get(user_id).keys() if rel_comment_dic.get(user_id) else [])

            rel_view_user_dic = rel_view_dic.get(user_id)
            rel_like_user_dic = rel_like_dic.get(user_id)
            rel_comment_user_dic = recommend_dic.get(user_id)
            for blog_id in blog_id_set:
                weight = 0.0
                if rel_view_user_dic and rel_view_user_dic.get(blog_id):
                    weight = weight + VIEW_WEIGHT * rel_view_user_dic[blog_id]
                if rel_like_user_dic and rel_like_user_dic.get(blog_id):
                    weight = weight + LIKE_WEIGHT * rel_like_user_dic[blog_id]
                if rel_comment_user_dic and rel_comment_user_dic.get(blog_id):
                    weight = weight + COMMENT_WEIGHT * rel_comment_user_dic[blog_id]
                recommend_dic[user_id][blog_id] = weight
        iron_log.info('end cal_recommend_list.')
        # 2.根据blogId查询forum.blog表,去除原始推荐列表中作者为用户本人的,私有权限的或已经删除的blogId,若结果数目大于10，则取前十条
        iron_log.info('start to save recommend_list...')
        # 先删除已有推荐结果
        Recommend_Result.objects.all().delete()
        for user_id, blog_dic in recommend_dic.items():
            max_item_num = 0
            for blog_id, weight in blog_dic.items():
                try:
                    blog = Blog.objects.using('forum').get(id=blog_id)
                    if blog.user_id == user_id or blog.is_private is True or blog.deleted is True:
                        continue
                    Recommend_Result(user_id=user_id, blog_id=blog_id, weight=weight).save()
                    max_item_num += 1
                    if max_item_num >= 10:
                        break
                except Exception, ex:
                    iron_log.exception(ex)
                    iron_log.error('Exception, task will continue.')

        iron_log.info('end save recommend_list.')
    except Exception, ex:
        iron_log.error('Exception!!!')
        iron_log.exception(ex)


def assemble_rel_dic_from_db(log_type):
    rel_model = LOG_MODEL_DIC.get(log_type).get(REL_MODEL)
    dic = {}
    page = 0
    size = 100
    rel_list = list(rel_model.objects.all()[page * size: (page + 1) * size])
    while len(rel_list) != 0:
        for rel in rel_list:
            if not dic.get(rel.user_id):
                dic[rel.user_id] = {}
            dic[rel.user_id][rel.blog_id] = rel.weight
        page += 1
        rel_list = list(rel_model.objects.filter()[page * size: (page + 1) * size])

    return dic


def assemble_train_dic_from_db(log_type):
    log_model = LOG_MODEL_DIC.get(log_type).get(MOVE_MODEL)
    train = {}
    page = 0
    size = 100
    log_list = list(log_model.objects.all()[page * size: (page + 1) * size])
    while len(log_list) != 0:
        for log in log_list:
            if not train.get(log.user_id):
                train[log.user_id] = {}
            train[log.user_id][log.blog_id] = log.weight
        page += 1
        log_list = list(log_model.objects.filter()[page * size: (page + 1) * size])

    return train


def save_rel_table(log_type, rel_table):
    log_model = LOG_MODEL_DIC.get(log_type).get(REL_MODEL)
    # 删除已有数据
    log_model.objects.all().delete()
    for user_id, blog_item in rel_table.items():
        if len(blog_item) > 0:
            for blog_id, weight in blog_item.items():
                log_model(user_id=user_id, blog_id=blog_id, weight=weight).save()


def apply_algorithm_and_save(log_type):
    iron_log.info('start to apply_algorithm_and_save...')
    iron_log.info('start to assemble_train_dic_from_db')
    train = assemble_train_dic_from_db(log_type)
    iron_log.info('assemble_train_dic_from_db done')
    iron_log.info('start to cal user_similarity')
    sim_table = user_cf.user_similarity(train)
    iron_log.info('cal user_similarity done')
    iron_log.info('start to cal rel_table')
    rel_table = {}
    for user_id in sim_table.keys():
        rel_table[user_id] = user_cf.Recommend(user_id, train, sim_table, 2)
    iron_log.info('cal rel_table done')
    iron_log.info('start to save_rel_table')
    if len(rel_table) > 0:
        save_rel_table(log_type=log_type, rel_table=rel_table)
    iron_log.info('save_rel_table done')
    iron_log.info('end apply_algorithm_and_save.')
