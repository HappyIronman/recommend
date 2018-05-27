# -*- coding: utf-8 -*-

import logging
from django.apps import AppConfig

iron_log = logging.getLogger('ironman')


class HomepageConfig(AppConfig):
    name = 'homepage'
    verbose_name = 'recommend'

    def ready(self):
        print 'hhh'
        from homepage import constants
        from apscheduler.scheduler import Scheduler
        from homepage.task import craw_news_task
        from homepage.engine import engine
        if constants.IS_READY:
            return
        constants.IS_READY = True
        iron_log.info('init PARTNER_ID_SET...')
        constants.PARTNER_ID_SET = set(constants.PARTNER_IDS.split(';'))
        iron_log.info(constants.PARTNER_ID_SET)
        sched = Scheduler()

        @sched.interval_schedule(seconds=60 * 20)
        def craw_news():
            craw_news_task.offline_craw()

        @sched.interval_schedule(seconds=60 * 30)
        def offline_cal_recommend_list_task():
            iron_log.info('start to offline_cal_recommend_list_task')
            engine.offline_cal_recommend_list()
            iron_log.info('end offline_cal_recommend_list_task\n')

        sched.start()

        craw_news()
        offline_cal_recommend_list_task()

# def init_partner_id_list():
#     iron_log.info('init PARTNER_ID_SET...')
#     constants.PARTNER_ID_SET = set(constants.PARTNER_IDS.split(';'))
#     iron_log.info(constants.PARTNER_ID_SET)
