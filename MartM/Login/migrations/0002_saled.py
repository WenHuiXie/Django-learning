# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Gapple', models.IntegerField()),
                ('Gorange', models.IntegerField()),
                ('Gbowl', models.IntegerField()),
                ('Gchopstick', models.IntegerField()),
                ('Grag', models.IntegerField()),
                ('Gtissue', models.IntegerField()),
                ('Gnoddle', models.IntegerField()),
                ('Gham', models.IntegerField()),
                ('Gdate', models.CharField(max_length=15)),
            ],
        ),
    ]
