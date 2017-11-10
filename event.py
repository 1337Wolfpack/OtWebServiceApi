from otQuery import otQuery
from ot_field import *

class event(object):
    def __init__(self):
        self.folder = r"01. ITSM - Service Operation\01. Event Management"
        self._id= ObjectId('objectId')
        self._UCID = StringVal('UCID')
        self._phone = StringVal('Phone Number')
        self._applicant = ReferenceToUserVal('Applicant')
        self._responsible = ReferenceToUserVal('Responsible')
        self._number = StringVal('Number')
        self._creationdate = DateTimeVal('CreationDate')
        self._enddate=DateTimeVal('CallFinishedDateTime')
        self._transferhistory = StringVal('TransferHistory')
        self.createdindatabase=False
        
 
    
    def create(self):
        self.id = otQuery()\
            .add(self.folder, [self._UCID,])
        self.createdindatabase=True

    def delete(self):
        otQuery().delete(self.id)
        
    @staticmethod
    def get(id):
        new_event = event()
        otQuery().get(new_event, id)
        return new_event

    @property
    def id(self):
        return self._id.value

    @id.setter
    def id(self, value):
        self._id.value = value

    @property
    def UCID(self):
        return self._UCID.value

    @UCID.setter
    def UCID(self, value):
        self._UCID.value = value
        otQuery().update(self, self._UCID)

    @property
    def phone(self):
        return self._phone.value

    @phone.setter
    def phone(self, value):
        self._phone.value = value
        otQuery().update(self, self._phone)

    @property
    def applicant(self):
        return self._applicant.value

    @applicant.setter
    def applicant(self, value):
        self._applicant.value = value
        otQuery().update(self, self._applicant)

    @property
    def responsible(self):
        return self._responsible.value

    @responsible.setter
    def responsible(self, value):
        self._responsible.value = value
        otQuery().update(self, self._responsible)

    @property
    def number(self):
        return self._number.value

    @number.setter
    def number(self, value):
        self._number.value = value
        otQuery().update(self, self._number)

    @property
    def transferhistory(self):
        return self._transferhistory.value

    @transferhistory.setter
    def transferhistory(self, value):
        self._transferhistory.value = value
        otQuery().update(self, self._transferhistory)

    @property
    def creationdate(self):
        return self._creationdate.value

    @creationdate.setter
    def creationdate(self, value):
        self._creationdate.value = value
        otQuery().update(self, self._creationdate)
        
    @property
    def enddate(self):
        return self._enddate.value

    @enddate.setter
    def enddate(self, value):
        self._enddate.value = value
        otQuery().update(self, self._enddate)
