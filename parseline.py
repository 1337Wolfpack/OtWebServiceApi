centrale = ["571", "572", "573"]
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OtWebServiceApi.settings")
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
from ot_webservice_api.models import Ot_config, Agent, Call, Ticket, Event
from event import event as ot_event
import time
import datetime
import re
from otQuery import otQuery
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
           
        except ObjectDoesNotExist:    
            return False
        call.end = getDateFromLine(line)
        call.save()
            
        if call.event != None:
            event = call.event
            event.end = call.end
            event.save()
                
            call.delete()
        
        
      
        
def handleEstablished(line, UCID):
    if 'Established Event, UCID<' in line:
       
        try:
            call = Call.objects.get(ucid=UCID)
            
    
        except ObjectDoesNotExist:    
            linedate = getDateFromLine(line)
            call = Call()
            print ("creating call %s" % UCID)
            call.start = linedate
            call.ucid = UCID
            call.save()
        call.state= 'established'        
        destination = getAnswererExt(line)
        if call.destination != destination:
            call.destination = destination
            if call.history == None:
                call.history = destination
            else:
                call.history = '%s -> %s' % (call.history , destination)
            call.save()
            
        call.save()
        if destination in centrale:
            call.agent = Agent.objects.get(displayname="Centrale")
            call.save()
        else:
            assignToAgent(call)
            

def assignToAgent(call):
        try:
            agent =  Agent.objects.get(phone=call.destination)
            if agent.is_helpdesk:
                call.agent = agent
        except ObjectDoesNotExist:
            outsidehd = True
        call.save()
    
    
    


        

def saveEvent(line, UCID):
    try:
        call = Call.objects.get(ucid=UCID)
    except ObjectDoesNotExist:
        return False
    if call.agent !=None:
    
        if call.event == None and call.agent.is_helpdesk:
            try:
                event = Event.objects.get(ucid=UCID)
            except ObjectDoesNotExist:
                event = Event()
                event.ucid = call.ucid
        
            event.start = call.start
            event.applicant = call.agent
            event.destination = call.destination
            event.origin = call.origin
            event.event_type = call.call_type
            event.history = call.history
            event.save()
            call.event = event
            call.save()
            if event.ot_id != "":
                ot_ev=otQuery().get(ot_event(), event.ot_id)
            else:
                ot_ev = ot_event()
                ot_ev.UCID = UCID
                ot_ev.create()
            
                event.ot_id = ot_ev.id
                event.save()
            ot_ev.phone = event.origin
            ot_ev.creationdate = event.start
            ot_ev.transferhistory=event.history
            ot_ev.applicant = event.applicant.login
            
            
            

        

    
def getCallType(line):
    index = line.find('CallTypeName:')
    callType= ""
    if index != -1:
        indexEnd = line.find(', Priority')
        callType = line[index + 13:indexEnd]
        return callType
            

def getCallerPhone(line):
    reg = re.compile('OriginalANI:[0-9]{4,18}')
    test = reg.search(line)
    callerPhone = ""
    if test:
        data = test.group()
        data = data.split(':')
        callerPhone = data[1]
    return callerPhone      
 
        
def getDetails(line, UCID):
    
    if 'UpdateRoutingData Event, UCID<' in line:
        try:
            call = Call.objects.get(ucid=UCID)
        except ObjectDoesNotExist:
            return False
    
        call.origin = getCallerPhone(line)
        call.call_type = getCallType(line)
        call.save()
        
        
def getCall(line):
    try:
        call = Call.objects.get(ucid=UCID)
    except ObjectDoesNotExist:
        return False
    return call



def parseline(line):
    UCID = findUCID(line)
    
    if UCID != '0':
        handleEstablished(line, UCID)
        getDetails(line, UCID)
        saveEvent(line, UCID)
        handleRemoved(line, UCID)

        #handleDetailsFound(line, UCID)

    