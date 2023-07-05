from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    # path('view/', views.cart_detail, name='cart_detail'),
    # path('update_quantity/<int:book_id>/', views.update_quantity, name='update_quantity'),
    # path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('create/',views.create_order, name='create_order'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('',views.order_list,name = 'order_list'),
    path('top_selling_books/',views.top_selling_books, name= 'top_selling_books'),
    path('sales_report/',views.sales_report, name= 'sales_report'),
    path('sales_report_genre/',views.sales_report_genre, name= 'sales_report_genre'),
    path('sales_report_author/',views.sales_report_author, name= 'sales_report_author'),
]
