# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-14 17:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0008_list'),
    ]

    operations = [
        migrations.DeleteModel(
            name='List',
        ),
    ]
