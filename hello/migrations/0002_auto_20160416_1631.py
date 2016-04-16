# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2016, 4, 16))),
                ('item', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, max_length=200)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2, default=0)),
                ('total', models.DecimalField(max_digits=100, decimal_places=2)),
                ('sites', models.ManyToManyField(to='sites.Site')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='greeting',
            name='when',
            field=models.DateTimeField(verbose_name='date created', auto_now_add=True),
        ),
    ]
