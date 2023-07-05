from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path("loin/",views.loin,name = "loin"),
    path('',views.home,name = 'home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_update, name='update_profile'),
    path('all_users/',views.all_user,name = 'all_users'),
]
