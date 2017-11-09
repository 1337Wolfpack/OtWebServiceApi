centrale = ["571", "572", "573"]
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OtWebServiceApi.settings")
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
from ot_webservice_api.models import Ot_config, Agent, Call, Ticket, Event
from event import event
import time
import datetime

def findUCID(line):
        UCID = '0'
        Ucid_index = line.find('UCID: ')

        if Ucid_index != -1:
            UCID = line[Ucid_index + 6:Ucid_index + 22]
        Ucid_index = line.find('UCID<')
        if Ucid_index != -1:
            UCID = line[Ucid_index + 5:Ucid_index + 21]
        Remove_Ucid_index = line.find('Removing UCID')
        if Remove_Ucid_index != -1:
            Ucid_index = line.find('UCID')
            UCID = line[Ucid_index + 5:Ucid_index + 22]
        update_Ucid_index = line.find('UpdateRoutingData Event')
        if update_Ucid_index != -1:
            Ucid_index = line.find('UCID<')
            UCID = line[Ucid_index + 5:Ucid_index + 21]

        return UCID

def getDateFromLine(line):

        datestr = line[1:20]
        structTime = time.strptime(datestr, '%Y/%m/%d %H:%M:%S')
        linedate = \
            datetime.datetime.fromtimestamp(time.mktime(structTime))
        return linedate

 
def getAnswererExt(line):
    index =  line.find('AnswerDID:')
    return line[index + 10:index + 13]
    
def handleRemoved(line, UCID):
    if 'Remove UCID<' in line:
        try:
            call = Call.objects.get(ucid=UCID)
            call.delete()
        except ObjectDoesNotExist:    
            print('call did not exist in DB')
        
        
      
        
def handleEstablished(line, UCID):
    if 'Established Event, UCID<' in line:
        try:
            call = Call.objects.get(ucid=UCID)
    
        except ObjectDoesNotExist:    
            linedate = getDateFromLine(line)
            call = Call()
            call.start = linedate
            call.ucid = UCID
            call.state= 'established'    
            call.save()
        call.state= 'established'        
        
        destination = getAnswererExt(line)
        if call.destination != destination:
            call.destination = destination
            call.history = '%s -> %s' % (call.history , destination)
            call.save()
        call.save()
        if call.destination in centrale:
            call.agent = Agent.objects.get(displayname="Centrale")
            call.save()
        else:
            assignToAgent(call)
            

def assignToAgent(call):
        try:
            call.agent = Agent.objects.get(phone=call.destination)
        except:
            print("no agent with ext %s" % call.destination)
        call.save()
        saveEvent(call)

def saveEvent(call):
    
    if call.event == None:
        event = Event()
        event.
    
    
        





def parseline(line):
    UCID = findUCID(line)
    if UCID != '0':
        handleEstablished(line, UCID)
        handleRemoved(line, UCID)
        #handleDetailsFound(line, UCID)

    