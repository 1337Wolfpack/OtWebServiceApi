from django.db import models
from django.contrib import admin
# Create your models here.


class Ot_config(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Agent(models.Model):
    login = models.CharField(max_length=200,null=True)
    displayname = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    is_helpdesk = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    phone = models.CharField(max_length=200,null=True)
    ot_id = models.CharField(max_length=200)
    def __str__(self):
        return self.displayname
        
class AgentAdmin(admin.ModelAdmin):
    list_display = ('displayname', 'first_name', 'last_name', 'phone', 'is_helpdesk')
  
class Call(models.Model):
    ucid = models.CharField(max_length=200, unique=True)
    state = models.CharField(max_length=200,null = True)
    origin = models.CharField(max_length=200,null = True)
    destination = models.CharField(max_length=200,null = True)
    call_type = models.CharField(max_length=200,null = True)
    start = models.DateTimeField(max_length=200,null = True)
    end = models.DateTimeField(max_length=200,null = True)
    history=models.CharField(max_length=600, null = True)
    agent = models.ForeignKey(Agent,null = True)
    
    def __str__(self):
        return self.ucid
        
        
class Ticket(models.Model):
    title = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    state = models.CharField(max_length=200)    
    applicant = models.ForeignKey(Agent, related_name = 'ticket_applicant')
    responsible = models.ForeignKey(Agent, related_name = 'ticket_responsible')
    ot_id = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
        
        
class Event(models.Model):
    ucid = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start = models.DateTimeField(max_length=200)
    end = models.DateTimeField(max_length=200)
    ticket = models.ForeignKey(Ticket)
    applicant = models.ForeignKey(Agent, related_name = 'event_applicant')
    responsible = models.ForeignKey(Agent, related_name = 'event_responsible')
    ot_id = models.CharField(max_length=200)
    event = models.ForeignKey(Call)
    
    def __str__(self):
        return self.UCID
        
