from django.db import models
from django.contrib.auth.models import User
from books.models import Book
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Processing'),
        (2, 'Shipped'),
        (3, 'Delivered'),
        (4, 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=0)
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address  = models.CharField(max_length=50)
    
    def get_order_total(self):
        order_items = OrderItem.objects.filter(order=self)
        total = 0
        for item in order_items:
            total += item.get_item_price()
        return total
    
class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_item_price(self):
        return self.book.price * self.quantity

