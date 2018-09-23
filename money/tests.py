# -*- coding: utf-8; -*-
__author__ = 'Vladimir'
from django.test import SimpleTestCase
from .models import Account
from .decorators import test_concurrently


class AccountTestCase(SimpleTestCase):
    user_id = 100
    amount = 30.0
    min_value = 10.0
    max_value = 50.0
    wrong_user_id = 200
    thread_num = 100

    def setUp(self):
        """Perform before each test."""
        Account.objects.create_account(user_id=self.user_id,
                                       amount=self.amount,
                                       min_value=self.min_value,
                                       max_value=self.max_value)

    def tearDown(self):
        """Perform after each test."""
        Account.objects.filter(user_id=self.user_id).delete()

    def test_get_change_amount(self):
        """Test for getting correct HTML form."""
        response = self.client.get('/money/change/')
        self.assertTemplateUsed(response=response, template_name='account.html')

    def test_post_change_amount_correct_increase(self):
        """Test for correct increase of amount."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': '10.0',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Update successful.<br>"
                                 "See log file for details.",
                            status_code=200)

    def test_post_change_amount_border_correct_increase(self):
        """Test for correct border increase of amount."""
        change = round(self.max_value - self.amount, 1)
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': str(change),
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Update successful.<br>"
                                 "See log file for details.",
                            status_code=200)

    def test_post_change_amount_border_correct_decrease(self):
        """Test for correct border increase of amount."""
        change = round(self.amount - self.min_value, 1)
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': str(change),
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Update successful.<br>"
                                 "See log file for details.",
                            status_code=200)

    def test_post_change_amount_correct_decrease(self):
        """Test for correct decrease of amount."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': '-10.0',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Update successful.<br>"
                                 "See log file for details.",
                            status_code=200)

    def test_post_change_amount_incorrect_increase(self):
        """Test for incorrect increase of amount (amount + change > max_value)."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': '100.0',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Update unsuccessful: out of bounds.<br>"
                                 "See log file for details",
                            status_code=400)

    def test_post_change_amount_incorrect_decrease(self):
        """Test for incorrect decrease of amount (amount - change < min_value)."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': '-100.0',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Update unsuccessful: out of bounds.<br>"
                                 "See log file for details",
                            status_code=400)

    def test_post_change_amount_empty_user_id_value(self):
        """Test for empty string user_id parameter."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': '',
                'change': '10.0',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Wrong value of argument 'user_id'.<br>"
                                 "See log file for details.",
                            status_code=400)

    def test_post_change_amount_empty_change_value(self):
        """Test for empty string change parameter."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': '',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Wrong value of argument change.<br>"
                                 "See log file for details.",
                            status_code=400)

    def test_post_change_amount_non_int_user_id_value(self):
        """Test for non-int user_id parameter."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': 'aAbB',
                'change': '10.0',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Wrong value of argument 'user_id'.<br>"
                                 "See log file for details.",
                            status_code=400)

    def test_post_change_amount_wrong_change_value(self):
        """Test for non-float change parameter."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.user_id),
                'change': 'cCdD',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Wrong value of argument 'change'.<br>"
                                 "See log file for details.",
                            status_code=400)

    def test_post_change_amount_wrong_user_id_value(self):
        """Test for incorrect user_id (no such user_id in database)."""
        response = self.client.post(
            '/money/change/',
            {
                'user_id': str(self.wrong_user_id),
                'change': '10.0',
                'log_test': True
            }
        )
        self.assertContains(response=response,
                            text="Wrong argument 'user_id' = {}<br>"
                                 "No such user in database."
                                 "".format(self.wrong_user_id),
                            status_code=400)

    def test_change_amount_threaded(self):
        """Test for any concurrency issues."""
        @test_concurrently(self.thread_num)
        def perform_change():
            response = self.client.post(
                '/money/change/',
                {
                    'user_id': str(self.user_id),
                    'change': '10.0',
                    'log_test': True
                }
            )
        perform_change()
