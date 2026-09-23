import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

# Host 'testserver' dipakai Django test client; izinkan agar bukan bug aplikasi
settings.ALLOWED_HOSTS = settings.ALLOWED_HOSTS + ["testserver"]

User = get_user_model()

publik = [
    "beranda",
    "komoditas",
    "komoditas_ekspor",
    "berita",
    "kontak",
    "profil",
    "layanan_teknis",
    "login",
    "register",
]
staff = [
    "dashboard_index",
    "harga_komoditas",
    "export_harga_csv",
    "kelola_komoditas",
    "kelola_berita",
    "kelola_kontak",
]

# buat staff user test jika belum ada
u, created = User.objects.get_or_create(
    username="checkertester",
    defaults={"is_staff": True, "is_active": True},
)
if created:
    u.set_password("testpass12345")
    u.save()

cli = Client()
cli.force_login(u)

print("== PUBLIC VIEWS ==")
for name in publik:
    try:
        url = reverse(name)
        r = cli.get(url)
        status = r.status_code
        flag = "OK " if status in (200, 302) else "FAIL"
        print(f"  [{flag}] {name:22s} {url:30s} -> {status}")
    except Exception as e:
        print(f"  [ERR ] {name:22s} {type(e).__name__}: {e}")

print("== STAFF VIEWS ==")
for name in staff:
    try:
        url = reverse(name)
        r = cli.get(url)
        status = r.status_code
        flag = "OK " if status in (200, 302) else "FAIL"
        print(f"  [{flag}] {name:22s} {url:30s} -> {status}")
        if status >= 500:
            print("        content snippet:", r.content[:300])
    except Exception as e:
        print(f"  [ERR ] {name:22s} {type(e).__name__}: {e}")

print("== DETAIL BERITA (perlu record) ==")
from berita.models import Berita  # noqa: E402
from komoditas.models import Komoditas  # noqa: E402

try:
    b = Berita.objects.first()
    if b:
        r = cli.get(reverse("berita_detail", args=[b.id]))
        print(f"  [{'OK ' if r.status_code==200 else 'FAIL'}] berita_detail id={b.id} -> {r.status_code}")
    else:
        print("  [skip] tidak ada record Berita")
except Exception as e:
    print(f"  [ERR ] berita_detail: {type(e).__name__}: {e}")

try:
    k = Komoditas.objects.first()
    if k:
        r = cli.get(reverse("edit_komoditas", args=[k.id]))
        print(f"  [{'OK ' if r.status_code in (200,302) else 'FAIL'}] edit_komoditas id={k.id} -> {r.status_code}")
    else:
        print("  [skip] tidak ada record Komoditas")
except Exception as e:
    print(f"  [ERR ] edit_komoditas: {type(e).__name__}: {e}")

print("== API ENDPOINTS ==")
for name in ["api_harga_komoditas", "api_daftar_komoditas", "api_daftar_berita"]:
    try:
        url = reverse(name)
        r = cli.get(url)
        ct = r.get("Content-Type", "")
        ok = r.status_code == 200 and "json" in ct
        print(f"  [{'OK ' if ok else 'FAIL'}] {name:24s} -> {r.status_code} {ct[:30]}")
    except Exception as e:
        print(f"  [ERR ] {name}: {type(e).__name__}: {e}")

# cleanup user test
u.delete()
print("\nDONE")
