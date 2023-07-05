from django.urls import path
from . import views

app_name = 'genres'

urlpatterns = [
    path('',views.all_genres,name = 'all_genres'),
    path('create/', views.genre_create, name='create'),
    path('details/<int:id>', views.genres_detail, name='details'),
]