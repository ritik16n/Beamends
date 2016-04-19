# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20160418_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='date',
            field=models.DateField(default=datetime.date(2016, 4, 19)),
        ),
    ]
