from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/logo.png', permanent=True)),
    path('admin/', admin.site.urls),
    path('', include('harga.urls')),
    path('', include('komoditas.urls')),
    path('', include('berita.urls')),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
]

if settings.DEBUG:
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)