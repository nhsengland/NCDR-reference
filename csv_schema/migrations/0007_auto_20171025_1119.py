# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_schema', '0006_auto_20171025_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='row',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='row',
            name='created_date_ext',
            field=models.DateField(blank=True, null=True),
        ),
    ]