from otQuery import otQuery
from ot_field import ObjectId, StringVal, ReferenceVal, DateTimeVal,\
    ReferenceToUserVal


class ticket(object):
    def __init__(self):
        self.folder = r"01. ITSM - Service Operation\02. Incident Management"
        self._id = ObjectId('objectId')
        self._title = StringVal('Title')
        self._description = StringVal('Description')
        self._category = ReferenceVal('AssociatedCategory')
        self._applicant = ReferenceToUserVal('Applicant')
        self._responsible = ReferenceToUserVal('Responsible')
        self._number = StringVal('Number')
        self._solutiondescription = StringVal('SolutionDescription')
        self._creationdate = DateTimeVal('CreationDate')

    def create(self):
        self.id = otQuery()\
            .add(self.folder, [self._title, self._description, self._category])

    def delete(self):
        otQuery().delete(self.id)

    @staticmethod
    def get(id):
        new_ticket = ticket()
        otQuery().get(new_ticket, id)
        return new_ticket

    @property
    def id(self):
        return self._id.value

    @id.setter
    def id(self, value):
        self._id.value = value

    @property
    def title(self):
        return self._title.value

    @title.setter
    def title(self, value):
        self._title.value = value
        otQuery().update(self, self._title)

    @property
    def description(self):
        return self._description.value

    @description.setter
    def description(self, value):
        self._description.value = value
        otQuery().update(self, self._description)

    @property
    def category(self):
        return self._category.value

    @category.setter
    def category(self, value):
        self._category.value = value
        otQuery().update(self, self._category)

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
    def solutiondescription(self):
        return self._solutiondescription.value

    @solutiondescription.setter
    def solutiondescription(self, value):
        self._solutiondescription.value = value
        otQuery().update(self, self._solutiondescription)

    @property
    def creationdate(self):
        return self._creationdate.value

    @creationdate.setter
    def creationdate(self, value):
        self._creationdate.value = value
        otQuery().update(self, self._creationdate)
