# bank
Test Task, which could be useful for some people, who work with Python and Django

There are users in the System, each user have an account - one float number.
Each user has min and max values for his/her account.
Balance of the account can't be bigger then max and smaller, then min.
Initial balance is equal to the min value.
Each second system receives huge number of requests for add some money or to charge-off.
Each request contains user's ID and amount of change (positive or negative float).
System must response with message which says, that balance was successfully changed or 
that there was some kind of issue.
There must be logging of all events.

Unit-tests are included.

Python 3, Django, MySQL