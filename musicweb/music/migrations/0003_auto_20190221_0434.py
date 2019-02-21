# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20190219_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='song_upload',
            field=models.FileField(default=b' ', upload_to=b''),
        ),
        migrations.AlterField(
            model_name='music',
            name='access',
            field=models.ForeignKey(to='music.Access'),
        ),
        migrations.AlterField(
            model_name='music',
            name='emotion',
            field=models.ForeignKey(to='music.Emotion'),
        ),
    ]
