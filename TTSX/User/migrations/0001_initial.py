# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Uname', models.CharField(max_length=20)),
                ('Upwd', models.CharField(max_length=40)),
                ('Uphont', models.CharField(max_length=11)),
                ('Umail', models.CharField(max_length=20)),
                ('Ushou', models.CharField(default=b'', max_length=10)),
                ('Uaddr', models.CharField(default=b'', max_length=100)),
                ('Ucode', models.CharField(default=b'', max_length=6)),
            ],
        ),
    ]
