"""recommend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import logging

from apscheduler.scheduler import Scheduler
from django.conf.urls import url
from django.contrib import admin

from homepage import views, constants
from homepage.engine import engine
from homepage.task import craw_news_task

iron_log = logging.getLogger('ironman')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test1/', views.test1),
    url(r'^recommend/homepage/', views.get_recommend_homepage),
]

sched = Scheduler()


@sched.interval_schedule(seconds=60 * 5)
def craw_news():
    craw_news_task.offline_craw()


@sched.interval_schedule(seconds=60 * 30)
def offline_cal_recommend_list_task():
    iron_log.info('start to offline_cal_recommend_list_task')
    engine.offline_cal_recommend_list()
    iron_log.info('end offline_cal_recommend_list_task\n')


sched.start()


def init_partner_id_list():
    iron_log.info('init PARTNER_ID_SET...')
    constants.PARTNER_ID_SET = set(constants.PARTNER_IDS.split(';'))
    iron_log.info(constants.PARTNER_ID_SET)


init_partner_id_list()
# craw_news()
# offline_cal_recommend_list_task()
