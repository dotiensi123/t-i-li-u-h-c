from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('books/<int:book_id>/reviews/new/', views.create_review, name='create_review'),
    path('reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('top_rated_books',views.top_rated_books, name='top_rated_books'),
    # path('books/reviews/count/', views.review_count, name='review_count'),
    # path('books/reviews/average/', views.review_average, name='review_average'),    
]