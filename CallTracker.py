# -*- coding: utf-8 -*-
import parseutils
import time
import logging
from eventchanges import *
from activecall import activecall
import os
import threading

import logger
log = logger.log()
helpdesk = [552, 540, 539, 528,530,511,534,509,535,553,566]
centrale = [571, 572, 573]

class parseLog(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # A flag to notify the thread that it should finish up and exit
        self.kill_received = False
        
        self.LogFile = r'\\ccrcsl02\ShareData\DIAGS\TelephonyServer_ccrcsl02.000'
        #self.LogFile = r'\\ccrcsl01\ShareData\DIAGS\TelephonyServer_ccrcsl01.000'
                    #LogFile = r'H:\testlog.txt'
        self.trackedEvents = []
        #self.f = open(self.LogFile)
        phoneLineState = "Up"
                #dictParsedLines= dict()
        self.dictActiveCalls = dict()
                
    
    def run(self):
        f= open(self.LogFile)
        filesize = os.stat(self.LogFile).st_size
        oldfilesize = filesize
        while not self.kill_received:
            filesize = os.stat(self.LogFile).st_size
            
            if filesize < oldfilesize:
                f.close()
                f = open(self.LogFile)
            #print filestats.st_size
            oldfilesize = filesize
            line=f.readline()
            time.sleep(.001)
            #log.info(line)
            parser = parseutils.parseutils(line)
            #We need data for a spcific UCID
            if 'UCID' in parser.parseditems.keys():
                
                UCID = parser.UCID
                
                #retrieving the call object for this UCID.
                events_results = otQuery().getObjectList(event, "EventUCID",[["UCID" , self.UCID],])
                
                if len(events_result) ==1:
                    activeCall = events.result[0]
                else:
                    activeCall = event()
                    activeCall.UCID = UCID
                
                #Finding out if we already manage this call in memory
                
                if activecall.
                
                if 'callhandledByExt' in parser.parseditems.keys():
                    #has it changed from previous call handler?
                    if activeCall.callhandledByExt != parser.parseditems['callhandledByExt']:
                        activeCall.callhandledByExt = parser.parseditems['callhandledByExt']
                        if activeCall.createdindatabase == False:
                            activeCall.create()
                            if activeCall.createdindatabase == True:
                                activeCall.creationdate = parser.parseditems['datetime']

                                
                        if activeCall.created==True:
                            activeCall.setCaller()
                            activeCall.changeHandler()
                    
                if 'transferedTo' in parser.parseditems.keys():
                    continue      
         
                 
                if 'callerPhone' in parser.parseditems.keys():
                    activeCall.callerPhone =  parser.parseditems['callerPhone']
                    if activeCall.created==True:
                        activeCall.setCaller()
                if 'finished' in parser.parseditems.keys():
                    activeCall.endDate = parser.parseditems['datetime']
                    if activeCall.created==True:
                        activeCall.setToFinished()
                    try:
                        del self.dictActiveCalls[UCID]
                    except:
                        print "already removed"
               
                
                if 'stateConsulting' in parser.parseditems.keys():
                    if parser.parseditems['consultingWith'] != "":
                        activeCall.state = "consulting"
                        activeCall.consultingWith = parser.parseditems['consultingWith']
                        if activeCall.created==True:
                            activeCall.consulting()
    
                
                
                self.dictActiveCalls[UCID] = activeCall
    
            else:
                if "Trunk 309 (grp 101) is out of service." in line:
                    phoneLineState = "Down"
                if "Trunk 309 (grp 101) is back in service" in line:
                    phoneLineState = "Up"
        
