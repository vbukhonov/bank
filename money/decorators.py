# -*- coding: utf-8; -*-
__author__ = 'Vladimir'
import threading

def test_concurrently(times):
    """
    This decorator is for small pieces of code that should be tested
    concurrently to make sure they don't raise exceptions when run at the
    same time.
    https://www.caktusgroup.com/blog/2009/05/26/testing-django-views-for-concurrency-issues/
    """
    def test_concurrently_decorator(test_func):
        def wrapper(*args, **kwargs):
            exceptions = []

            def call_test_func():
                try:
                    test_func(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    raise

            threads = []
            for i in range(times):
                threads.append(threading.Thread(target=call_test_func))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            if exceptions:
                raise Exception('test_concurrently intercepted %s exceptions: %s' % (len(exceptions), exceptions))
        return wrapper
    return test_concurrently_decorator