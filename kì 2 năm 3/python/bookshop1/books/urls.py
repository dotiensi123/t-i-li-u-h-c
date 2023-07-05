from django.urls import path
from . import views
app_name = 'books'
urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('search/', views.book_search, name='book_search'),
]