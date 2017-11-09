import xml.etree.ElementTree as ET
import otXmlPost   
from ticket import ticket
from event import event
from user import user
from otQuery import otQuery


helpdesk = [552, 540, 539, 528,530,511,534,509,535,553,566]
centrale = [571, 572, 573]

agentlist = otQuery.getObjectList(user,"", [])



class activecall():
       
    Calls = []
    
    def __init__(self):
        self.UCID = ""
        self.callType = ""
        self.callerPhone = ""
        self.startDate = ""
        self.endDate = ""
        self.finished = False
        self.callhandledByExt="572"
        self.consultingWith=""
        self.stateConsulting = False
        self.state = ""
        self.history = ""
        self.otEventId= ""    
        self.created = False
        self.external = False
        self.agentList = agentList
        self.agent = ""
        self.callPickedUpdateTime = ""
        

        
    
    def createnew(self):
        self.createNewEvent()
        print "Calls active : %s" % len(self.Calls)
        
    def changeHandler(self):
        #print "change target of call to " + self.callhandledByExt + " for UCID " + self.UCID
        self.history = "%s -> %s" % (self.history, self.callhandledByExt) 
        self.state = "normal"
        self.changeEventApplicant()


        
    def changeState(self):
        print "change state of call to " + self.state
        		
    def consulting(self):
        print "consulting with " + self.consultingWith
        self.history = "%s -> consulting with %s" % (self.history, self.consultingWith) 
    
    def setToFinished(self):
        self.callFinished()
        print "finished %s" % self.endDate

        
        
    def findEventForUCID(self):
        
        if self.otEventId =="":
            
            an_event = otQuery().getObjectList(event, "EventUCID",[["UCID" , self.UCID],])
            self.otEventId = an_event.id
            return an_event.id            
        else:
            return self.otEventId
        return False 
             

 
    #===========================================================================
    # def findEventForUCID(self):
    #     if self.otEventId =="":
    #         ot= otXmlPost.otXml()
    #         XmlResponse = ot.queryObjects(r'01. ITSM - Service Operation\01. Event Management', ["UCID",])
    #         tree = ET.fromstring(XmlResponse)
    #         root= tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
    #         for child in root:
    #     #print child.attrib['id']
    #             for attribute in child:
    #                 if attribute.get('name') =='UCID':
    #                     if self.UCID== attribute.text:
    #                         return child.attrib['id']
    
    #     else:
    #         return self.eventId
    #     return False 
    #===========================================================================
    def definePickedUpDate(self):
	    
            ot= otXmlPost.otXml()
            #XmlResponse= ot.modifyEvent('DateTimeVal', findEventForUCID(UCID), 'CallFinishedDateTime','2014/08/04T15:30:12')
            XmlResponse= ot.modifyEvent('DateTimeVal', self.findEventForUCID(), 'PickUpDateTime','%s' % self.callPickedUpdateTime.isoformat())
    
    def findAgentFromExt(self):
        
        username=""
        for agent in self.agentlist:
            if agent.phone[0]=="-":
                ext = ext[1:4]
            if ext == self.callhandledByExt:
                return self.login
        #
    def modifyCreationDate(self):
        
        ot= otXmlPost.otXml()
        
        #XmlResponse= ot.modifyEvent('DateTimeVal', findEventForUCID(UCID), 'CallFinishedDateTime','2014/08/04T15:30:12')
        XmlResponse= ot.modifyEvent('DateTimeVal', self.findEventForUCID(), 'Creation Date','%s' % self.startDate.isoformat())
      
        #print "Creation Date Modified : %s" % XmlResponse
    
    def setCaller(self):
        ot= otXmlPost.otXml()
        if len(self.callerPhone) >0:
            if self.callerPhone[0] == "0":
            
                XmlResponse= ot.modifyEvent('StringVal', self.findEventForUCID(), 'Phone Number','%s' % self.callerPhone[1:])
        else:
            XmlResponse= ot.modifyEvent('StringVal', self.findEventForUCID(), 'Phone Number','%s' % self.callerPhone)
      	#print "Phone Number Modified : %s" % XmlResponse
    
    def callFinished(self):
        
        try : 
            self.Calls.remove(self)
        except:
            print self.Calls
        
        if self.finished != True:
            
            
            ot= otXmlPost.otXml()
        
            #XmlResponse= ot.modifyEvent('DateTimeVal', findEventForUCID(UCID), 'CallFinishedDateTime','2014/08/04T15:30:12')
            XmlResponse= ot.modifyEvent('DateTimeVal', self.findEventForUCID(), 'CallFinishedDateTime','%s' % self.endDate.isoformat())
            #print "End Date Modified : %s" % XmlResponse
            ot= otXmlPost.otXml()
            XmlResponse = ot.modifyEvent('StringVal', self.findEventForUCID(), 'TransferHistory','%s' % self.history)
            #print "history modified : %s, %s" % (XmlResponse, self.history)
            self.finished = True
            self.state = "finished"
            
        
        
        
    def changeEventApplicant(self):
        
        if int(self.callhandledByExt) in helpdesk:
            ot= otXmlPost.otXml()
            XmlResponse = ot.modifyEventRef('userloginname',self.findEventForUCID(),'Applicant', self.findAgentFromExt())
            self.agent = self.findAgentFromExt()
            
            #print XmlResponse
        if int(self.callhandledByExt) in centrale:
            ot= otXmlPost.otXml()
            self.callhandledByExt = "572"
            XmlResponse = ot.modifyEventRef('userloginname',self.findEventForUCID(),'Applicant', self.findAgentFromExt())
            self.agent = self.findAgentFromExt()
        
    def createNewEvent(self):
        
            
        #list of helpdesk people :
        

        if int(self.callhandledByExt) in helpdesk and self.external == True:
            #self.Calls.append(self)
        #if int(self.callhandledbyExt) > 500 and int(self.callhandledbyExt()) <573:
            
            if self.created==False:
            
                eventAlreadyExists = self.findEventForUCID()
                if eventAlreadyExists == False:
                    ot= otXmlPost.otXml()
                    XmlResponse = ot.addEvent(self.UCID)
                    tree = ET.fromstring(XmlResponse)
                    root= tree.find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')
                    EventId = root.attrib['objectId']
                    print "DEBUG : %s" % EventId
                    if EventId > 0:
                        self.otEventId = EventId
                #print XmlResponse
                        self.created = True
                else:
                #print "Event already created"
                    self.created=True

        if int(self.callhandledByExt) in centrale:
            self.Calls.append(self)
            if self.created==False:
                eventAlreadyExists = self.findEventForUCID()
                if eventAlreadyExists == False:
                    ot= otXmlPost.otXml()
                    XmlResponse = ot.addEvent(self.UCID)
                    tree = ET.fromstring(XmlResponse)
                    root= tree.find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')
                    EventId = root.attrib['objectId']
                    print "DEBUG : %s" % EventId
                    if EventId > 0:
                        self.otEventId = EventId
                #print XmlResponse
                        self.created = True
                else:
                #print "Event already created"
                    self.created=True
            self.external = True
            self.state = "Centrale"
      