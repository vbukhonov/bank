# -*- coding: utf-8; -*-
__author__ = 'Vladimir'

from django.db.models import Manager


class AccountManager(Manager):
    """Manager for Accounts"""
    def create_account(self, user_id, min_value, max_value, amount=None):
        if amount is None:
            amount = min_value
        if min_value > max_value:
            raise Exception("Wrong borders!")
        if amount > max_value:
            raise Exception("Wrong amount (more than max)!")
        if amount < min_value:
            raise Exception("Wrong amount (less than min)!")
        return self.create(user_id=user_id, amount=amount, min_value=min_value, max_value=max_value)
