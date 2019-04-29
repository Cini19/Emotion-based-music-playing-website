# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0003_auto_20190221_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='emotion',
            name='emo_pic',
            field=models.FileField(default=b' ', upload_to=b''),
        ),
        migrations.AddField(
            model_name='music',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
