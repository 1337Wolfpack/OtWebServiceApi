import time
import datetime
from ticket import ticket


currticket = ticket()
currticket.title = "Ceci est un test ticket"
currticket.category = "1154755"
currticket.description ="test description"
currticket.create()
currticket.title = "test de changement de titre2"

print currticket.title
print currticket.id
currticket.creationdate = datetime.datetime.now()


print currticket.creationdate
currticket = ticket.get(currticket.id)

print currticket.creationdate

print "ticket created, deleting in 20 secs"
time.sleep(20)
currticket.delete()


