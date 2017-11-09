import xml.etree.ElementTree as ET
#from collections import namedtuple
from ot_field import ot_field, ObjectId, StringVal, ReferenceVal,\
    DateTimeVal, ReferenceToUserVal

import requests
import platform
import dateutil.parser
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OtWebServiceApi.settings")
import django
django.setup()
from ot_webservice_api.models import Ot_config
config = Ot_config.objects.all()[0]
url = config.url



if platform.system() == "Windows":
    Encoding = "cp437"
else:
    Encoding = "utf-8"
    
    






class otQuery():
    def __init__(self):
        self.body = ""
        self.xml = r""
        self.command = ""
        self.result = ""
        self.success = False
        self.xml_result = ""

    def initQuery(self):
        self.headers = {'Content-Type': 'text/xml', 'charset': 'iso-8859-1',
                        'SOAPAction': '"http://www.omninet.de/OtWebSvc/v1/%s"'
                        % (self.command)}
        self.xml = r'<?xml version="1.0" encoding="utf-8"?><soap:Envelope ' + \
            r'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + \
                   r'xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' + \
                   r'xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Body>' + \
                   r'<%s xmlns="http://www.omninet.de/OtWebSvc/v1">' % (self.command) + \
                   r'%s</%s></soap:Body></soap:Envelope>' \
                   % (self.body, self.command)

    def sendQuery(self):
        data = self.xml.replace(r'\r\n', r'&#x000d;&#x000a;').encode("ascii", "xmlcharrefreplace")
        result = requests.post(url, data=data, headers=self.headers)
        self.xml_result = result.content
        return self

    def add(self, folder, fields):
        id = False
        self.body = ""
        self.command = "AddObject"
        xmlstring = self.getfieldXmlString(fields)
        self.body = r'%s<Object folderPath="%s">' % (self.body, folder) + \
            r'%s' % xmlstring
        self.body = '%s</Object>' % self.body
        self.initQuery()
        self.sendQuery()
        tree = ET.fromstring(self.xml_result)
        root = tree \
            .find('*//{http://www.omninet.de/OtWebSvc/v1}AddObjectResult')
        if root.attrib['success'] == "true":
            id = root.attrib['objectId']
        else:
            print("couldn't add item in %s with fields %s" % (folder, fields))
            print("request : %s" % self.xml)
            print("response : %s" % self.xml_result)
        return id

    def buildObject(self, item):

        tree = ET.fromstring(self.xml_result)
        root = tree \
            .find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
        if root.attrib['success'] == "true":
            self.result = True
            root = root[0]
            item.id = root.attrib['id']
            for property, value in vars(item).items():
                if isinstance(value, ot_field):
                    properties = root.findall(".//*[@name='%s']" % value.name)
                    if len(properties) > 0:
                        var = properties[0]
                        value.value = self.\
                            convAttributeforPython(value,
                                                   value.getValueFromXML(var))
        else:
            print("couldn't build complete query : %s" % (item))
            print("request : %s" % self.xml)
            print("response : %s" % self.xml_result)

        return item


    def get(self, item, id):
        if item.id != "":
            id = item.id
        self.body = ""
        self.command = "GetObjectList"
        self.body = r'%s<Get folderPath="%s" recursive="true"><ObjectIDs objectIDs="%s"/>'\
            % (self.body, item.folder, id)
        for property, value in vars(self).items():
            if isinstance(value, ot_field) and value.name != "objectId":
                self.body = r'%s<RequiredField>%s</RequiredField>' \
                % (self.body, value.name)
        self.body = "%s</Get>" \
        % (self.body)
        self.initQuery()
        self.sendQuery()
        item = self.buildObject(item)
        return item
    
    

    
    
    def getObjectList(self, objectclass, filter, variables):
        self.body = ""

        item=objectclass()
        self.command = "GetObjectList"
        self.body = r'%s<Get folderPath="%s" recursive="true">' \
        % (self.body, item.folder)
        if filter != "":
        
            self.body = '%s<Filter>%s' % (self.body, filter)
            filterVars = ''
            for variable in variables:
                filterVars =  '%s<%s name="%s">%s</%s>' % (filterVars, 'StringVal', variable[0], variable[1], 'StringVal')
            self.body = '%s%s</Filter>' % (self.body, filterVars)
        
    
        RequiredFields = []
        
        
        #for key, value in vars(item).items():
        #    if isinstance(value, ot_field) and value.name != "objectId":
        #        RequiredFields.append(value)
        
        
         
        
        
        #<Filter>EventUCID<StringVal name="UCID">%s</StringVal></Filter>
        for field in RequiredFields:
            self.body = r'%s<RequiredField>%s</RequiredField>' \
            % (self.body, field.name)
        self.body = "%s</Get>" % (self.body)
        self.initQuery()
        self.sendQuery()
        
        
        result = self.buildobjects(objectclass)
        #print(self.xml)
        return result
    
    def buildobjects(self, objectclass):
        results = []
        tree = ET.fromstring(self.xml_result)
        print(self.xml_result)
        root = tree \
            .find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
        if root.attrib['success'] == "true":
            for child in root:
                item = objectclass()
                #ET.dump(child)
                item.id = child.attrib['id']
                if item.id == "44620":
                    ET.dump(child)
                for property, value in vars(item).items():
                    if isinstance(value, ot_field):
                        properties = child.findall(".//*[@name='%s']" % value.name)
                        #print('finding field %s' % value.name)
                        #print (properties)
                        if len(properties) > 0:
                            var = properties[0]
                            value.value = self.\
                                convAttributeforPython(value,
                                                       value.getValueFromXML(var))
                            #print (value.value)
            
                results.append(item)
            
        return results
    
    
    

    def convAttributeforPython(self, field, value):
        if isinstance(field, DateTimeVal):
            #print("converting " + value)
            return dateutil.parser.parse(value)
        else:
            return value

    def convAttributeforOT(self, field):
        if isinstance(field, DateTimeVal):
            return field.value.isoformat()
        else:
            return field.value

    def getItem(self, item, field):
        self.body = ""
        self.command = "GetObjectList"
        self.body = r'%s<Get folderPath="%s" recursive="true"><ObjectIDs objectIDs="%s"/>' \
        % (self.body, self.folder, item.id.value)
        self.body = r'%s<RequiredField>%s</RequiredField>' \
        % (self.body, field.name)
        self.body = "%s</Get>" % (self.body)
        self.initQuery()
        self.sendQuery()

        tree = ET.fromstring(self.xml_result)
        root = tree.find('*//{http://www.omninet.de/OtWebSvc/v1}GetObjectListResult')
        print("looking for property %s" % field)
        if root.attrib['success'] == "true":
            self.result = True
            root = root[0]
            properties = root.findall(".//*[@name='%s']" % field.name)
            print(properties[0])
            if len(properties) > 0:

                return field.getValueFromXML(properties[0])
        else:

            print("couldn't build complete query : %s : %s" % (item, field))
            print("request : %s" % self.xml)
            print("response : %s" % self.xml_result)

    def update(self, item, field):
        value = self.convAttributeforOT(field)
        if item.id == "":
            return False
        self.body = ""
        self.command = "ModifyObject"
        self.body = r'%s<Object objectId="%s">' % (self.body, item.id)
        self.body = r'%s<%s name="%s">%s</%s>' \
            % (self.body, field.fieldtype, field.name, value, field.fieldtype)
        self.body = "%s</Object>" % (self.body)
        self.initQuery()
        self.sendQuery()
        print(self.xml)
        print(self.xml_result)
        tree = ET.fromstring(self.xml_result)
        root = tree\
            .find('*//{http://www.omninet.de/OtWebSvc/v1}ModifyObjectResult')
        if root.attrib['success'] == "true":
            self.result = True
        else:
            print("couldn't build update object : %s : %s" % (item, field))
            print("request : %s" % self.xml)
            print("response : %s" % self.xml_result)
        return self.result

    def delete(self, id):
        self.body = ""
        self.command = "RemoveObject"
        self.body = r'%s<ObjectID>%s</ObjectID><IgnoreReferences>true</IgnoreReferences>' \
            % (self.body, id)
        self.initQuery()
        self.sendQuery()
        tree = ET.fromstring(self.xml_result)
        root = tree\
            .find('*//{http://www.omninet.de/OtWebSvc/v1}RemoveObjectResult')
        if root.attrib['success'] == "true":
            self.result = True
        else:
            print("couldn't build update object : %s : %s" % (item, field))
            print("request : %s" % self.xml)
            print("response : %s" % self.xml_result)
        return self.result

    def getfieldXmlString(self, fields):
        fieldxml = ""
        for field in fields:
            fieldxml = "%s%s" % (fieldxml, field.fieldXMLString(field.name))
        return fieldxml
