# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-10 10:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170210_0200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippinginvoice',
            name='isd_code',
        ),
        migrations.RemoveField(
            model_name='shippinginvoice',
            name='isd_name',
        ),
    ]