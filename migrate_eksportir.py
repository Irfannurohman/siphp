from komoditas.models import Komoditas, Eksportir
from harga.models import HargaKomoditas

koms = Komoditas.objects.filter(is_ekspor=True)
count = 0
for k in koms:
    try:
        h = HargaKomoditas.objects.filter(komoditas=k).order_by('-tanggal').first()
        vol = h.harga if h else 0
        Eksportir.objects.get_or_create(
            profil_company=k.nama, 
            komoditas=k.kategori or "Unknown", 
            defaults={'volume': vol, 'satuan': k.satuan, 'tujuan_ekspor': k.keterangan or ""}
        )
        k.delete()
        count += 1
    except Exception as e:
        print(f"Error migrating {k.nama}: {e}")

print(f"Migrated {count} records.")
