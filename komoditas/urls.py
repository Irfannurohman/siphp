from django.urls import path
from . import views

urlpatterns = [
    path('komoditas/', views.komoditas, name='komoditas'),
    path('komoditas/ekspor/', views.komoditas_ekspor, name='komoditas_ekspor'),
    path('dashboard/komoditas/', views.kelola_komoditas, name='kelola_komoditas'),
    path('dashboard/komoditas/edit/<int:id>/', views.edit_komoditas, name='edit_komoditas'),
    path('dashboard/komoditas/hapus/<int:id>/', views.hapus_komoditas, name='hapus_komoditas'),
    path('dashboard/eksportir/', views.kelola_eksportir, name='kelola_eksportir'),
    path('dashboard/eksportir/edit/<int:id>/', views.edit_eksportir, name='edit_eksportir'),
    path('dashboard/eksportir/hapus/<int:id>/', views.hapus_eksportir, name='hapus_eksportir'),
    path('api/komoditas/', views.api_daftar_komoditas, name='api_daftar_komoditas'),
]
