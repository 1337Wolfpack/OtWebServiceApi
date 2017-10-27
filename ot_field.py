class ot_field(object):
    def __init__(self, name):
        self.fieldtype = ""
        self.name = name
        self.value = ""

    def fieldXMLString(self, fieldname):
        fieldquery = r'<%s name="%s">%s</%s>' \
            % (self.fieldtype, fieldname, self.value, self.fieldtype)
        return fieldquery

    def getValueFromXML(self, xml):
        return xml.text

    def __unicode__(self):
        return self.value


class ObjectId(ot_field):
    def __init__(self, name):
        super(ObjectId, self).__init__(name)
        self.fieldtype = "ID"


class StringVal(ot_field):
    def __init__(self, name):
        super(StringVal, self).__init__(name)
        self.fieldtype = "StringVal"


class DateTimeVal(ot_field):
    def __init__(self, name):
        super(DateTimeVal, self).__init__(name)
        self.fieldtype = "DateTimeVal"


class Text(ot_field):
    def __init__(self, name):
        super(Text, self).__init__(name)
        self.fieldtype = "Text"


class ReferenceVal(ot_field):
    def __init__(self, name):
        super(ReferenceVal, self).__init__(name)
        self.fieldtype = "ReferenceVal"

    def fieldXMLString(self, fieldname):
        fieldquery = r'<ReferenceVal name="%s" objectId="%s"/>' \
            % (self.name, self.value)
        return fieldquery

    def getValueFromXML(self, xml):
        return xml.attrib['objectId']


class ReferenceToUserVal(ot_field):
    def __init__(self, name):
        super(ReferenceToUserVal, self).__init__(name)
        self.fieldtype = "ReferenceVal"
        self.reference = "userloginname"

    def fieldXMLString(self, fieldname):
        fieldquery = r'<ReferenceToUserVal name = "%s" type = "%s" Value = "%s" />' \
            % (self.fieldtype, self.reference, self.value)
        return fieldquery

    def getValueFromXML(self, xml):
        return xml.attrib['Value']

