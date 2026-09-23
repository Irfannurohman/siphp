from django.contrib import admin
from .models import Komoditas, Eksportir


@admin.register(Komoditas)
class KomoditasAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "kategori", "satuan", "keterangan")
    list_filter = ("kategori",)
    search_fields = ("nama", "kategori")


@admin.register(Eksportir)
class EksportirAdmin(admin.ModelAdmin):
    list_display = ("profil_company", "komoditas", "volume", "satuan", "tujuan_ekspor")
    search_fields = ("profil_company", "komoditas", "tujuan_ekspor")