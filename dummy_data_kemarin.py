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
yesterday = today - datetime.timedelta(days=1)

markets = Pasar.objects.all()
komoditas_list = Komoditas.objects.all()

count = 0
for p in markets:
    print(f"Mengisi data kemarin untuk {p.nama_pasar}...")
    for k in komoditas_list:
        # Ambil harga hari ini jika ada
        harga_today_obj = HargaKomoditas.objects.filter(komoditas=k, pasar=p, tanggal=today).first()
        if harga_today_obj:
            harga_today = harga_today_obj.harga
            
            # Buat harga kemarin bervariasi:
            # 40% kemungkinan lebih tinggi (harga turun hari ini)
            # 40% kemungkinan lebih rendah (harga naik hari ini)
            # 20% kemungkinan sama (stabil)
            rand = random.random()
            if rand < 0.4:
                dummy_price_yesterday = harga_today + (random.randint(1, 10) * 500)
            elif rand < 0.8:
                dummy_price_yesterday = max(500, harga_today - (random.randint(1, 10) * 500))
            else:
                dummy_price_yesterday = harga_today
                
            HargaKomoditas.objects.update_or_create(
                komoditas=k, 
                pasar=p, 
                tanggal=yesterday, 
                defaults={'harga': dummy_price_yesterday}
            )
            count += 1

print(f"BERHASIL MENGINPUT {count} DATA KEMARIN UNTUK {markets.count()} PASAR!")
