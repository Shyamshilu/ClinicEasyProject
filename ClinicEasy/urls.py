from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", account_views.home, name="index"),

    path('', include('accounts.urls')),
    path('', include('doctors.urls')),
    
    path('admin-panel/', include('adminpanel.urls')),
    path('appointment/', include('appointments.urls')),
    path('service-details/<str:name>/', account_views.service_details, name='service-details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
