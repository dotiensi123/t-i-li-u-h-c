from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    
    def get_item_total(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.user.username}'s cart item: {self.book.title}"
