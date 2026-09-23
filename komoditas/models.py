from django.db import models


class Komoditas(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    kategori = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kategori")
    satuan = models.CharField(max_length=20, default="kg")
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "accounts_komoditas"
        verbose_name_plural = "Komoditas"
        ordering = ["nama"]

    def __str__(self):
        return f"{self.nama} ({self.satuan})"

class Eksportir(models.Model):
    profil_company = models.CharField(max_length=200, verbose_name="Profil Company")
    komoditas = models.CharField(max_length=100, verbose_name="Komoditas")
    volume = models.FloatField(default=0, verbose_name="Volume Pengiriman Ekspor")
    satuan = models.CharField(max_length=20, default="kg", verbose_name="Satuan")
    tujuan_ekspor = models.CharField(max_length=200, verbose_name="Tujuan Ekspor")

    class Meta:
        db_table = "accounts_eksportir"
        verbose_name_plural = "Daftar Eksportir"
        ordering = ["profil_company"]

    def __str__(self):
        return f"{self.profil_company} - {self.komoditas}"