# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-21 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_gasStation_map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotmodel',
            name='end_date',
            field=models.DateField(default='', verbose_name='Fecha final'),
        ),
        migrations.AlterField(
            model_name='plotmodel',
            name='initial_date',
            field=models.DateField(default='', verbose_name='Fecha de inicio'),
        ),
    ]