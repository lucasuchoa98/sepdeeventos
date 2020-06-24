from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'eventodef'

urlpatterns = [
    path('', views.home, name='home'),
    path('resultado/', views.result_view, name='resultado'),
    path(r'download/<str:path>/', views.download_file, name='download')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)