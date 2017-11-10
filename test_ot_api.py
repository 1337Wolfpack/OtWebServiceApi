#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
from ticket import ticket
from user import user
from event import event

from otQuery import otQuery
currticket = ticket()
currticket.title = 'Ceci est un test ticket'
currticket.category = '1154755'
currticket.description = 'test description'
currticket.create()
currticket.title = 'test de changement de titre2'

print currticket.title
print currticket.id
currticket.creationdate = datetime.datetime.now()

print currticket.creationdate
currticket = ticket.get(currticket.id)

print currticket.creationdate

print 'ticket created, deleting in 2 secs'
time.sleep(2)
currticket.delete()

filter = 'internal-issues-group-all'
variables = [['username', 'LeBourg Julien']]

# results = otQuery().getObjectList(ticket, filter, variables)
# for result in results:
#    print(result.title)

filter = ''
results = otQuery().getObjectList(user, filter, variables)

for result in results:
    print result.login

currevent = event()
currevent.UCID = '2132134142341'
currevent.create()
currevent.phone = '21234'
currevent.delete()


			