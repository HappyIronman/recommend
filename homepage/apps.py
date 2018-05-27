# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommend.settings")
django.setup()

import logging

from apscheduler.scheduler import Scheduler
from django.apps import AppConfig

from homepage import constants
from homepage.engine import engine
from homepage.task import craw_news_task

iron_log = logging.getLogger('ironman')
sched = Scheduler()


class HomepageConfig(AppConfig):
    name = 'homepage'
    verbose_name = 'recommend'

    def ready(self):
        init_partner_id_list()
        craw_news()
        offline_cal_recommend_list_task()
        sched.start()


@sched.interval_schedule(seconds=60 * 5)
def craw_news():
    craw_news_task.offline_craw()


@sched.interval_schedule(seconds=60 * 30)
def offline_cal_recommend_list_task():
    iron_log.info('start to offline_cal_recommend_list_task')
    engine.offline_cal_recommend_list()
    iron_log.info('end offline_cal_recommend_list_task\n')


def init_partner_id_list():
    iron_log.info('init PARTNER_ID_SET...')
    constants.PARTNER_ID_SET = set(constants.PARTNER_IDS.split(';'))
    iron_log.info(constants.PARTNER_ID_SET)
