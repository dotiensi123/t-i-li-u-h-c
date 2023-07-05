from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from books.models import Book
from .models import Cart

@login_required(login_url='users:login')
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart_detail')

@login_required(login_url='users:login')
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        item.price = item.book.price * item.quantity
        total_price += item.price
    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='users:login')
def update_quantity(request, book_id):
    quantity = request.POST.get('quantity')
    cart_item = get_object_or_404(Cart, pk=book_id, user=request.user)
    if quantity and quantity.isdigit() and int(quantity) > 0 and int(quantity) <= 10:
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('cart:cart_detail')

@login_required(login_url='users:login')
def remove_from_cart(request, book_id):
    cart_item = get_object_or_404(Cart, pk=book_id, user=request.user)
    cart_item.delete()
    return redirect('cart:cart_detail')
