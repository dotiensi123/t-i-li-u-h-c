from django.db import models
from books.models import Book
from django.contrib.auth.models import User

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()

    class Meta:
        db_table = "book_reviews"
