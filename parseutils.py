#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import re
import logger
log = logger.log()


# requests_log = logging.getLogger("requests")
# requests_log.setLevel(logging.WARNING)

class parseutils:

    def __init__(self, line):
        self.line = line
        self.parseditems = dict()
        self.callType = ''
        self.callerPhone = ''
        self.transferedTo = ''
        self.finished = False
        self.callhandledByExt = ''
        self.callConsultingWith = ''
        self.stateConsulting = False

        self.UCID = self.findUCID().replace(' ', '')

        if self.UCID != '0':
            self.date = self.getDateFromLine()
            self.getDetails()
            self.getTransfer()
            self.getEstablished()
            self.getRemoved()
            self.getRetrieved()
            self.getConsult()

    def getCallType(self):
        CallTypeNameindex = self.line.find('CallTypeName:')
        if CallTypeNameindex != -1:
            IndexEnd = self.line.find(', Priority')
            self.callType = self.line[CallTypeNameindex + 13:IndexEnd]
            self.parseditems['callType'] = self.callType
            log.info('found call type : ' + self.callType)

    def getCallerPhone(self):
        reg = re.compile('OriginalANI:[0-9]{4,18}')
        test = reg.search(self.line)
        if test:
            data = test.group()
            data = data.split(':')
            self.callerPhone = data[1]
            self.parseditems['callerPhone'] = self.callerPhone
            log.info('found ' + self.callerPhone)

    def getTransfer(self):
        if 'Transferred Event, UCID' in self.line and 'LCS: Connected' \
                in self.line:
            Transfered_index = self.line.find('TransferToDID:')
            ext = self.line[Transfered_index + 14:Transfered_index + 17]
            self.transferedTo = ext
            self.parseditems['transferedTo'] = self.transferedTo
            self.stateConsulting = False
            self.consultingWith = ''
            self.parseditems['stateConsulting'] = self.stateConsulting
            self.parseditems['consultingWith'] = self.consultingWith
            log.info('got transferred to ' + ext)

    def getEstablished(self):
        if 'Established Event, UCID<' in self.line:
            Established_index = self.line.find('AnswerDID:')
            self.callhandledByExt = self.line[Established_index
                                              + 10:Established_index + 13]
            self.parseditems['callhandledByExt'] = self.callhandledByExt
            log.info('got established to ' + self.callhandledByExt)

    def getRemoved(self):
        if 'Removing UCID' in self.line:
            self.finished = True
            self.parseditems['finished'] = self.finished
            log.info('got removed call notification')
        if 'Remove UCID<' in self.line:
            self.finished = True
            self.parseditems['finished'] = self.finished
            log.info('got removed call notification')

    def getRetrieved(self):
        if 'Retrieved Event, UCID<' in self.line:
            self.stateConsulting = False
            self.consultingWith = ''
            self.parseditems['stateConsulting'] = self.stateConsulting
            self.parseditems['consultingWith'] = self.consultingWith
            Retrieving_index = self.line.find('RetrievingDID:')
            self.callhandledByExt = self.line[Retrieving_index
                                              + 14:Retrieving_index + 17]
            self.parseditems['callhandledByExt'] = self.callhandledByExt
            log.info('retrieving call to %s' % self.callhandledByExt)

            return True

    def getConsult(self):
        if 'Originated Event, UCID<%s' % self.UCID in self.line:
            if 'LCS:Connected, Cause:Consultation' in self.line:
                self.stateConsulting = True
                index = self.line.find('CalledDID:')

                ext = self.line[index + 10:index + 13]
                log.info('consulting call to ' + ext)

                if int(ext) > 500 and int(ext) < 571:
                    self.consultingWith = ext
                    self.parseditems['consultingWith'] = \
                        self.consultingWith
                    self.parseditems['stateConsulting'] = \
                        self.stateConsulting

            # Originated Event, UCID: 5971407401599172, RqC: 0, SubjectDID: 534(S), OriginatedCID: 244181, OriginatedDID: 534(S), CalledDID: 514(S), LCS: Connected, Cause: Consultation, Trunk: 534

            return True

    def getDetails(self):
        if 'UpdateRoutingData Event, UCID<' in self.line:
            self.getCallerPhone()
            self.getCallType()

    def getDateFromLine(self):

        datestr = self.line[1:20]
        structTime = time.strptime(datestr, '%Y/%m/%d %H:%M:%S')
        parsed = \
            datetime.datetime.fromtimestamp(time.mktime(structTime))
        self.parseditems['datetime'] = parsed
        return parsed

    def findUCID(self):
        UCID = '0'
        Ucid_index = self.line.find('UCID: ')

        if Ucid_index != -1:
            UCID = self.line[Ucid_index + 6:Ucid_index + 22]
        Ucid_index = self.line.find('UCID<')
        if Ucid_index != -1:
            UCID = self.line[Ucid_index + 5:Ucid_index + 21]
        Remove_Ucid_index = self.line.find('Removing UCID')
        if Remove_Ucid_index != -1:
            Ucid_index = self.line.find('UCID')
            UCID = self.line[Ucid_index + 5:Ucid_index + 22]
        update_Ucid_index = self.line.find('UpdateRoutingData Event')
        if update_Ucid_index != -1:
            Ucid_index = self.line.find('UCID<')
            UCID = self.line[Ucid_index + 5:Ucid_index + 21]
        if UCID != '0':
            self.parseditems['UCID'] = UCID
        if UCID != '0':
            log.info('found UCID:' + UCID)
        return UCID

