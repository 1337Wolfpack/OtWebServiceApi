from django.shortcuts import render
from django.http import HttpResponse
from ot_webservice_api.models import Call, Agent

from django.core.exceptions import ObjectDoesNotExist


def index(request):
    activeCalls = Call.objects.filter(state='established')
    Agents = Agent.objects.filter(is_helpdesk=True, active=True)
    FreeAgents = []
    busyExt = []
    html = \
        '<html><script>setTimeout(function(){ location.reload(); }, 1000);</script><body><table>'
    for call in activeCalls:
        busyExt.append(call.destination)
        busyExt.append(call.origin)
        if call.isContactCenterCall:
            html = '%s<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>' \
                % (html, call.origin, call.destination, call.state)
    for agent in Agents:
        if agent.phone not in busyExt:
            FreeAgents.append(agent)
    html = '%s</table>' % html
    result = ''
    for agent in FreeAgents:
        result = '%s,%s' % (result, agent)
    result = result[1:]

    html = '%s<p>%s</p>' % (html, result)

    return HttpResponse(html)

