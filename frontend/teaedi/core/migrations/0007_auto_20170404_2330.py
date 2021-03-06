# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 04:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170210_0451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesperson',
            name='school',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='sales_id',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='salesperson',
        ),
        migrations.AlterField(
            model_name='shippinginvoice',
            name='invoice_status',
            field=models.CharField(choices=[('I', 'Imported'), ('RP', 'Ready for Processing'), ('P', 'Processed'), ('A', 'Accepted'), ('E', 'Accepted with Error'), ('R', 'Rejected')], default='I', max_length=2),
        ),
        migrations.DeleteModel(
            name='SalesPerson',
        ),
        migrations.DeleteModel(
            name='School',
        ),
    ]
