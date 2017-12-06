#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author:Yanxin Zhang
from django.conf.urls import url
from . import views
from .feeds import LatestPostFeed
urlpatterns = [
    url(r'^$',views.post_list,name='post_list'),
    #url(r'^$',views.PostListView.as_view(),name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail,name='post_detail'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.post_list,name='post_list_by_tag'),
    url(r'^feed/$',LatestPostFeed(),name='post_feed'),
]



