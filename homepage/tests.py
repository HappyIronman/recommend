# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import datetime
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommend.settings")  # project_name 项目名称
django.setup()

from django.conf import settings

from homepage.engine import engine
from homepage.task import craw_news_task

# Create your tests here.
import logging

# Get an instance of a logger
root = logging.getLogger('ironman')
# logger = logging.getLogger(__name__)

if __name__ == '__main__':
    craw_news_task.offline_craw()
    engine.offline_cal_recommend_list()
