# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class CrawNews(models.Model):
    CSDN = 'CSDN'
    BKY = 'BKY'
    ORIGIN_SITE_CHOICES = (
        (CSDN, 'CSDN.net'),
        (BKY, '博客园'),
    )
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    pub_date = models.CharField(null=True, max_length=100)
    url = models.CharField(max_length=300)
    author = models.CharField(max_length=50, null=True)
    origin_site = models.CharField(max_length=10, choices=ORIGIN_SITE_CHOICES)
    create_time = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Rel_View(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    weight = models.FloatField()


class Move_View(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    weight = models.FloatField()


class Rel_Like(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    weight = models.FloatField()


class Move_Like(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    weight = models.FloatField()


class Rel_Comment(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    weight = models.FloatField()


class Move_Comment(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    weight = models.FloatField()


class Recommend_Result(models.Model):
    user_id = models.IntegerField()
    blog_id = models.IntegerField()
    weight = models.FloatField()


class View_Log(models.Model):
    user_id = models.IntegerField()
    target_id = models.IntegerField()
    type = models.IntegerField()
    length = models.IntegerField()
    disabled = models.BooleanField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'view_log'


class Like_Log(models.Model):
    user_id = models.IntegerField()
    target_id = models.IntegerField()
    type = models.IntegerField()
    is_like = models.BooleanField()
    disabled = models.BooleanField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'like_log'


class Comment(models.Model):
    user_id = models.IntegerField()
    reply_id = models.IntegerField()
    type = models.IntegerField()
    deleted = models.BooleanField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'comment'


class Blog(models.Model):
    unique_id = models.CharField(max_length=100)
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=3000, null=True)
    like_num = models.IntegerField
    dislike_num = models.IntegerField
    share_num = models.IntegerField
    comment_num = models.IntegerField
    view_num = models.IntegerField
    is_private = models.BooleanField()
    is_share = models.IntegerField
    deleted = models.BooleanField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'blog'


class User(models.Model):
    unique_id = models.CharField(max_length=100)
    username = models.CharField(max_length=40)

    class Meta:
        db_table = 'user'
