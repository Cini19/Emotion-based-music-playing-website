from django.conf.urls import url
from . import views


urlpatterns = [
    #/music/
    url(r'^$', views.Index, name='index'),
    #signup
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #login
    url(r'^login_user/$', views.LoginUser, name='login_user'),
    #logout
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    #/music/song/add/
    url(r'song/add/$', views.SongCreate, name='song-add'),
    #/music/my_song/
    url(r'^my_song/$', views.MySong, name='my-song'),
    #/music/my_song/2/delete
    url(r'^my_song/(?P<pk>[0-9]+)/delete/$', views.SongDelete.as_view(), name='song-delete'),
    #/include/3/detail/
    url(r'^(?P<emotion_id>[0-9]+)/detail/$', views.detail, name='detail'),
    #/music/detect/
    url(r'^detect/$', views.detect, name='detect'),
]

