# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20160416_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='date',
            field=models.DateField(default=datetime.date(2016, 4, 18)),
        ),
    ]
