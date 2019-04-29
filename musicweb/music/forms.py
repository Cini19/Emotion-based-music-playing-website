from django.contrib.auth.models import User
from django import forms
from .models import Music

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class MusicForm(forms.ModelForm):

    class Meta:
        model = Music
        fields = ['music_title', 'song_upload','access','emotion']


