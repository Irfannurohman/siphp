from berita.forms import BeritaForm

form = BeritaForm(data={"judul": "Test"})
print("IS VALID:", form.is_valid())
print("ERRORS:", form.errors)
