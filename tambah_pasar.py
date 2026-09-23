import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Pasar

markets = [
    'Pasar Baru Subang', 
    'Pasar Impres Pagaden', 
    'Pasar Impres Pamanukan', 
    'Pasar Ciasem', 
    'Pasar Purwadadi', 
    'Pasar Cisalak'
]

print("Menambahkan data pasar...")
for m in markets:
    obj, created = Pasar.objects.get_or_create(nama_pasar=m)
    if created:
        print(f"[+] Pasar ditambahkan: {m}")
    else:
        print(f"[-] Pasar sudah ada: {m}")

print("Selesai!")
