# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 14:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ot_webservice_api', '0010_event_ucid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='call',
        ),
    ]