# -*- coding: utf-8; -*-
__author__ = 'Vladimir'
import logging
import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import F
from .models import Account


def change_amount(request):
    """
    Change 'amount' parameter for selected user's account if possible.

    When first come to this view by GET, return simple HTML form
    with two text inputs: user_id and change.
    After submitting form, POST request is sent
    with values of those two arguments.
    Return simple 'Success!' or 'Failure' message,
    depending on whether the change was performed or not.
    All attempts are logged with standard logging tool.
    Arguments from POST:
    user_id -- ID of user whose account is changed, default value is 0.
    change -- the float number (positive or negative) which is used
              to change the "amount" field of selected user's account.
              It should satisfy:
              min_value <= amount + change <= max_value,
              where "min_value" and "max_value" are fields of selected user's account,
              'min_value' is minimum value of 'amount',
              'max_value' is maximum value of 'amount'.
    """
    if request.method == "POST":
        log_test = bool(request.POST.get('log_test', False))
        # In order to keep app clean, point logger to separate money_test.log file.
        # Get an instance of a logger.
        if log_test:
            logger = logging.getLogger('money_test')
        else:
            logger = logging.getLogger(__name__)
        str_datetime_and_status_code = str(datetime.datetime.now()) + " " + \
                                       str(HttpResponseBadRequest.status_code)
        # Get the user's id and the change value from POST.
        try:
            user_id = int(request.POST.get('user_id'))
        except Exception as e:
            logger.error(str_datetime_and_status_code +
                         " Wrong value of argument 'user_id'. " +
                         str(type(e).__name__) + ": " + str(e))
            return HttpResponseBadRequest("Wrong value of argument 'user_id'.<br>"
                                          "See log file for details.")
        try:
            change = float(request.POST.get('change'))
        except Exception as e:
            logger.error(str_datetime_and_status_code +
                         " Wrong value of argument 'change'. " +
                         str(type(e).__name__) + ": " + str(e))
            return HttpResponseBadRequest("Wrong value of argument 'change'.<br>"
                                          "See log file for details.")
        # Filter for selected user's account.
        # This is safe, because no new accounts are created or deleted.
        user_account = Account.objects.filter(user_id=user_id)
        if not user_account:
            logger.error(str_datetime_and_status_code +
                         " Wrong value of argument 'user_id' = " + str(user_id) + ". "
                         "No such user in database.")
            return HttpResponseBadRequest("Wrong argument 'user_id' = " + str(user_id) + "<br>"
                                          "No such user in database.")
        # The following part works fine and there will be no race condition,
        # because filter + update is performed as atomic.
        if change < 0.0:
            updated = user_account.filter(amount__gte=F('min_value') - change).update(amount=F('amount') + change)
            out_of_bounds_message = "new value is smaller, than minimum value."
        else:
            updated = user_account.filter(amount__lte=F('max_value') - change).update(amount=F('amount') + change)
            out_of_bounds_message = "new value is bigger, than maximum value."
        # Write log message and return HttpResponse or HttpResponseBadRequest,
        # where the text of message depends on the fact
        # if update was successful or not.
        # Python logging module is thread-safe by default.
        message = "user: " + str(user_id) + ", " + \
                  "change: " + str(change) + ", "
        # Here time is refreshed in order to fix it better.
        if updated:
            logger.info(str(datetime.datetime.now()) + " " +
                        str(HttpResponse.status_code) + " " +
                        message +
                        "update successful.")
            return HttpResponse("Update successful.<br>"
                                "See log file for details.")
        else:
            logger.error(str(datetime.datetime.now()) + " " +
                         str(HttpResponseBadRequest.status_code) + " " +
                         message +
                         "update unsuccessful: " + out_of_bounds_message)
            return HttpResponseBadRequest("Update unsuccessful: out of bounds.<br>"
                                          "See log file for details")
    # return simple html form in response to GET request
    return render(request, "account.html")
