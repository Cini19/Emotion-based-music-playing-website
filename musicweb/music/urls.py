from django.conf.urls import url
from . import views

urlpatterns = [
    #/music/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #signup
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #/music/song/add/
    url(r'song/add/$', views.SongCreate.as_view(), name='song-add'),
]
