#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'OtWebServiceApi.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
from otQuery import otQuery
from user import user

# your imports, e.g. Django models

from ot_webservice_api.models import Ot_config, Agent
config = Ot_config.objects.all()[0]
print config.url

userlist = otQuery().getObjectList(user, '', [])

for user in userlist:
    print user.displayname
    try:
        agent = Agent.objects.get(ot_id=user.id)
    except ObjectDoesNotExist:

        agent = Agent()
        agent.login = user.login

        # print(user.__dict__)

        agent.displayname = user.displayname
        agent.first_name = user.firstname
        agent.last_name = user.lastname
        if user.phone is None:
            agent.phone = ''
        else:
            agent.phone = user.phone[1:]
        agent.ot_id = user.id
        agent.save()


			