from komoditas.models import Komoditas

# The dummy export items that were previously masquerading as standard commodities
dummy_names = [
    "PT. Surya Seafood Mas",
    "PT. Hasil Tangkap Bahari",
    "CV. Unggas Nusantara",
    "PT. Ekspor Tani Makmur"
]

count = 0
for name in dummy_names:
    kom_qs = Komoditas.objects.filter(nama=name)
    for kom in kom_qs:
        kom.delete()
        count += 1
        
print(f"Deleted {count} leftover dummy export commodities from the Komoditas table.")
