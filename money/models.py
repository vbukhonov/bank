# -*- coding: utf-8; -*-
__author__ = 'Vladimir'
from django.db.models import Model, AutoField, IntegerField, FloatField
from .managers import AccountManager


class Account(Model):
    id = AutoField(primary_key=True, db_column='ID')
    user_id = IntegerField(unique=True, db_column='USER_ID', verbose_name='ID пользователя')
    amount = FloatField(db_column='AMOUNT', verbose_name='Сумма')
    min_value = FloatField(db_column='MIN_VALUE', verbose_name='Нижний порог')
    max_value = FloatField(db_column='MAX_VALUE', verbose_name='Верхний порог')

    class Meta:
        db_table = 'ACCOUNT'
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'
        ordering = ('user_id',)

    objects = AccountManager()
