# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql', '0002_auto_20210526_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='role',
            field=models.CharField(choices=[('工程师', '工程师'), ('审核人', '审核人')], default='工程师', max_length=20),
        ),
    ]
