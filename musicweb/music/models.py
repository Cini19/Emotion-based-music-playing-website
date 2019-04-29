from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse

from django_random_queryset import RandomManager


class Emotion(models.Model):
    emotion = models.CharField(max_length=10)
    emo_pic = models.FileField(default=' ')

    def __str__(self):
        return self.emotion+'-'+str(self.id)

class Access(models.Model):
    access = models.CharField(max_length=10)

    def __str__(self):
        return self.access+'-'+str(self.id)

class Music(models.Model):
    objects = RandomManager()
    emotion = models.ForeignKey(Emotion,on_delete=models.CASCADE)
    access = models.ForeignKey(Access,on_delete=models.CASCADE)
    music_title = models.CharField(max_length=40)
    song_upload = models.FileField(default=' ')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.music_title

    def get_absolute_url(self):
        return reverse('my-song')
