import os
import django
import datetime
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from harga.models import HargaKomoditas
from komoditas.models import Komoditas
from accounts.models import Pasar

today = datetime.date.today()
markets = Pasar.objects.all()
komoditas_list = Komoditas.objects.all()

count = 0
for p in markets:
    print(f"Mengisi data untuk {p.nama_pasar}...")
    for k in komoditas_list:
        # Harga acak antara 5.000 s/d 100.000 (kelipatan 500) agar terlihat realistis
        dummy_price = random.randint(10, 200) * 500 
        HargaKomoditas.objects.update_or_create(
            komoditas=k, 
            pasar=p, 
            tanggal=today, 
            defaults={'harga': dummy_price}
        )
        count += 1

print(f"BERHASIL MENGINPUT {count} DATA SEMENTARA UNTUK {markets.count()} PASAR!")
