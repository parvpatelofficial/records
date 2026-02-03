from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('school/', include('students.urls')),
    path('academics/', include('academics.urls')),
    path('attendance/', include('attendance.urls')),
    path('reports/', include('reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
