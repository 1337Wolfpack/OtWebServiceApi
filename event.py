from otQuery import otQuery
from ot_field import *

class event(object):
    def __init__(self):
        self.folder = r"01. ITSM - Service Operation\02. Incident Management"
        self._id= ObjectId('objectId')
        self._applicant = ReferenceToUserVal('Applicant')
        self._responsible = ReferenceToUserVal('Responsible')
        self._number = StringVal('Number')
        self._creationdate = DateTimeVal('CreationDate')


