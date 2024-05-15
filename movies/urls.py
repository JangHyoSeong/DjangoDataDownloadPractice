from django.urls import path
from . import views
import requests

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('actor/', views.actor, name='actor'),
    path('movielist/', views.download_movie_list, name='movie_list'),
]
