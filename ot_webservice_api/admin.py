from django.contrib import admin

# Register your models here.




from ot_webservice_api.models import Ot_config, Agent, Call, Ticket, Event
from ot_webservice_api.models import AgentAdmin, EventAdmin

admin.site.register(Ot_config)
admin.site.register(Agent,AgentAdmin)
admin.site.register(Call)
admin.site.register(Ticket)
admin.site.register(Event,EventAdmin)
