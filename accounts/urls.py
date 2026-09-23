from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/users/', views.kelola_users, name='kelola_users'),
    path('ubah-password/', views.ubah_password, name='ubah_password'),
]