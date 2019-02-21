from django.contrib import admin
from .models import Music, Emotion, Access

admin.site.register(Music)
admin.site.register(Access)
admin.site.register(Emotion)