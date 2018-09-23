# -*- coding: utf-8; -*-
__author__ = 'Vladimir'

from django.conf.urls import url
from .views import change_amount

urlpatterns = [
    url(r'^change/$', change_amount, name='change_money_amount'),
]
