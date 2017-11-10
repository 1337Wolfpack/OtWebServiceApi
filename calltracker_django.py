# -*- coding: utf-8 -*-

import time
import os
import threading

from parseline import parseline

class parseLog(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
        self.kill_received = False
        
        self.LogFile = r'/media/callcenter/DIAGS/TelephonyServer_ccrcsl02.000'
        self.trackedEvents = []
        phoneLineState = "Up"
        self.dictActiveCalls = dict()
                
    
    def run(self):
        num_lines = sum(1 for line in open(self.LogFile))
        f= open(self.LogFile)
        filesize = os.stat(self.LogFile).st_size
        oldfilesize = filesize

        line_nb = 1
        
        while not self.kill_received:
            filesize = os.stat(self.LogFile).st_size      
            if filesize < oldfilesize: #check if file has been rotated
                f.close()
                f = open(self.LogFile)
            oldfilesize = filesize
            line=f.readline()
            if line != "":
                line_nb = line_nb + 1
                parseline(line)
                time.sleep(.001)
                if line_nb < num_lines:
                    print("log at line %s of %s" % (line_nb, num_lines)) 
                else:
                    print("log at line %s" % line_nb) 


parseLog().run()
