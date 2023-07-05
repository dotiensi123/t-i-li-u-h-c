from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('',views.all_authors,name = 'all_authors'),
    path('create/', views.author_create, name='create'),
    path('update/<int:pk>/', views.author_update, name='update'),
    path('<int:pk>/', views.author_detail,name = 'detail'),
    path('book/<int:id>/', views.author_book, name = 'book'),
]
