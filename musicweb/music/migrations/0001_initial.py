# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('emotion', models.CharField(max_length=10)),
                ('access', models.CharField(max_length=20)),
                ('music_title', models.CharField(max_length=40)),
            ],
        ),
    ]
