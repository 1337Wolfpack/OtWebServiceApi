from otQuery import otQuery
from ot_field import ObjectId, StringVal, ReferenceVal, DateTimeVal,\
    ReferenceToUserVal


class user(object):
    def __init__(self):
        self.folder = r"00. MasterData\05. People\05.1 Persons\User Accounts"
        self._id = ObjectId('objectId')
        self._firstname = StringVal('FirstName')
        self._lastname = StringVal('LastName')
        self._phone = StringVal('Phone')
        self._login = StringVal('Login Name')
        self._displayname = StringVal('Title')

   
    @staticmethod
    def get(id):
        a_user = user()
        otQuery().get(a_user, id)
        return new_user

    @property
    def id(self):
        return self._id.value
    @id.setter
    def id(self, value):
        self._id.value = value
    @property
    def firstname(self):
        return self._firstname.value

    @property
    def lastname(self):
        return self._lastname.value

    
    @property
    def phone(self):
        return self._phone.value

    @phone.setter
    def phone(self, value):
        self._phone.value = value
        otQuery().update(self, self._phone)
      
    @property
    def login(self):
        return self._login.value
    
    @property
    def displayname(self):
        return self._displayname.value
    

   
      