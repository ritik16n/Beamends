# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20160420_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='item',
            field=models.CharField(max_length=20, verbose_name='stuff bought'),
        ),
    ]
