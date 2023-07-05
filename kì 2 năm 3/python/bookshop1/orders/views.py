from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from carts.models import Cart
from django.db.models import Sum
from books.models import Book
from django.contrib.auth.decorators import user_passes_test

@login_required(login_url='users:login')
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'order_list.html', {'orders': orders})

@login_required(login_url='users:login')
def create_order(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        order = Order.objects.create(user=user, full_name=full_name, phone_number=phone_number, address=address)
        for item in cart_items:
            OrderItem.objects.create(book=item.book, order=order, quantity=item.quantity)
        order.save()
        cart_items.delete()
        return redirect('orders:order_detail', order_id=order.pk)
    total_price = 0
    for item in cart_items:
        item.price = item.book.price * item.quantity
        book = Book.objects.get(pk=item.book.pk)
        book.stock -= item.quantity
        total_price += item.price
    return render(request, 'create_order.html', {'cart_items': cart_items,'total_price':total_price})

@login_required(login_url='users:login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order_items = order.orderitem_set.all()
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

def top_selling_books(request):
    books = Book.objects.annotate(total_sold=Sum('orderitem__quantity')).order_by('-total_sold')[:10]
    return render(request, 'book_list.html', {'books': books,})

@login_required(login_url='users:login')
@user_passes_test(lambda user: user.is_superuser)
def sales_report(request):
    confirmed_orders = Order.objects.filter(status=0)
    sales = []
    for order in confirmed_orders:
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            book_id = item.book.id
            existing_sale = next((sale for sale in sales if sale['book_id'] == book_id), None)
            if existing_sale:
                existing_sale['quantity'] += item.quantity
                existing_sale['total_price'] += item.get_item_price()
            else:
                sales.append({
                    'book_id': book_id,
                    'title': item.book.title,
                    'quantity': item.quantity,
                    'total_price': item.get_item_price(),
                    'price': item.book.price,
                    'genre': item.book.genre.name
                })

    total_sales = sum(sale['total_price'] for sale in sales)

    context = {
        'sales': sales,
        'total_sales': total_sales,
    }

    return render(request, 'sales_report.html', context)

@login_required(login_url='users:login')
@user_passes_test(lambda user: user.is_superuser)
def sales_report_genre(request):
    confirmed_orders = Order.objects.filter(status=0)
    sales = {}
    for order in confirmed_orders:
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            book_genre = item.book.genre
            if book_genre in sales:
                sales[book_genre]['quantity'] += item.quantity
                sales[book_genre]['total_price'] += item.get_item_price()
            else:
                sales[book_genre] = {
                    'genre_name': book_genre.name,
                    'quantity': item.quantity,
                    'total_price': item.get_item_price()
                }
    for book_genre in sales:
        sales[book_genre]['avg_price'] = sales[book_genre]['total_price'] / sales[book_genre]['quantity']
    total_sales = sum(item['total_price'] for item in sales.values())
    total_book = sum(item['quantity'] for item in sales.values())
    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_book': total_book,
    }
    return render(request, 'sales_report_genre.html', context)

@login_required(login_url='users:login')
@user_passes_test(lambda user: user.is_superuser)
def sales_report_author(request):
    confirmed_orders = Order.objects.filter(status=0)
    sales = {}
    for order in confirmed_orders:
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            book_author = item.book.author
            if book_author in sales:
                sales[book_author]['quantity'] += item.quantity
                sales[book_author]['total_price'] += item.get_item_price()
            else:
                sales[book_author] = {
                    'author_name': book_author.name,
                    'quantity': item.quantity,
                    'total_price': item.get_item_price()
                }
    for book_author in sales:
        sales[book_author]['avg_price'] = sales[book_author]['total_price'] / sales[book_author]['quantity']
    total_sales = sum(item['total_price'] for item in sales.values())
    total_book = sum(item['quantity'] for item in sales.values())
    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_book': total_book,
    }
    return render(request, 'sales_report_author.html', context)
