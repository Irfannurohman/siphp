import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Pasar

to_delete = ['Pasar Panjang', 'Pasar Pujasera']

for nama in to_delete:
    # Coba cari yang mirip case-insensitive menggunakan '__icontains'
    pasars = Pasar.objects.filter(nama_pasar__icontains=nama)
    if pasars.exists():
        for p in pasars:
            p.delete()
            print(f"[+] Berhasil menghapus: {p.nama_pasar}")
    else:
        print(f"[-] Tidak ditemukan pasar dengan nama mirip: {nama}")
