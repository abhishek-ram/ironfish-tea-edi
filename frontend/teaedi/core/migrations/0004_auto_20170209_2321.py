# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-10 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_purchaseorderline_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='processing_error_txt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_status',
            field=models.CharField(choices=[('O', 'Open'), ('P', 'Processed'), ('E', 'Processing Error'), ('C', 'Cancelled'), ('M', 'Modified')], default='O', max_length=2),
        ),
    ]
