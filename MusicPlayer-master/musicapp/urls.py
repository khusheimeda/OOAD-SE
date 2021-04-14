from django.urls import path
from . import views

# Add URLConf
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:song_id>/', views.detail, name='detail'),
    path('mymusic/', views.mymusic, name='mymusic'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<str:playlist_name>/', views.playlist_songs, name='playlist_songs'),
    path('favourite/', views.favourite, name='favourite'),
    path('all_songs/', views.all_songs, name='all_songs'),
    path('recent/', views.recent, name='recent'),
    path('hindi_songs/', views.hindi_songs, name='hindi_songs'),
    path('english_songs/', views.english_songs, name='english_songs'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('play_song/<int:song_id>/', views.play_song_index, name='play_song_index'),
    path('play_recent_song/<int:song_id>/', views.play_recent_song, name='play_recent_song'),
    path('max_played_songs/<int:song_id>/', views.play_song_max, name='play_song_max'),
    path('liked_songs/<int:song_id>/', views.play_liked_song, name='play_liked_song'),
    path('liked_songs/', views.liked_songs, name='liked_songs'),
    path('max_played_songs/', views.max_played_songs, name='max_played_songs'),
    path('recent_recommended/<int:song_id>/', views.play_recentcomm_song, name='play_recentcomm_song'),
    path('recent_recommended/', views.recent_recommended, name='recent_recommended'),


]
