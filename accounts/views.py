from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard_index")

    if request.method == "POST":
        username_req = request.POST.get("username")
        password_req = request.POST.get("password")

        user = authenticate(
            request, username=username_req, password=password_req
        )

        if user is not None:
            login(request, user)
            messages.success(
                request, f"Selamat datang kembali, {user.username}!"
            )
            return redirect("dashboard_index")
        else:
            messages.error(request, "Username atau password salah!")

    return render(request, "auth_custom/login.html")


def user_logout(request):
    logout(request)
    messages.info(request, "Anda telah berhasil keluar.")
    return redirect("beranda")


def register(request):
    if request.user.is_authenticated:
        return redirect("harga_komoditas")

    if request.method == "POST":
        username_req = request.POST.get("username")
        email_req = request.POST.get("email")
        password_req = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password_req != password_confirm:
            messages.error(request, "Konfirmasi password tidak cocok!")
            return render(request, "auth_custom/register.html")

        if User.objects.filter(username=username_req).exists():
            messages.error(request, "Username sudah terdaftar!")
            return render(request, "auth_custom/register.html")

        user = User.objects.create_user(
            username=username_req, email=email_req, password=password_req
        )
        user.save()
        messages.success(request, "Pendaftaran berhasil! Silakan login.")
        return redirect("login")

    return render(request, "auth_custom/register.html")


@login_required
def kelola_users(request):
    if not request.user.is_superuser:
        messages.error(request, "Anda tidak memiliki akses ke halaman tersebut.")
        return redirect('dashboard_index')
        
    users = User.objects.all().order_by('-date_joined')
    return render(request, "admin_dashboard/kelola_users.html", {'users': users})


@login_required
def ubah_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Anda berhasil diubah!')
            return redirect('dashboard_index')
        else:
            messages.error(request, 'Terdapat kesalahan. Silakan periksa kembali.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'auth_custom/ubah_password.html', {'form': form})