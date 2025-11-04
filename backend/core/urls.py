from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),    
    path('stationery/', include('stationery.urls')),
]

# serve media and static in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# including testing routes only in DEBUG (safe, non-production)
if settings.DEBUG:
    urlpatterns += [
        path('testing/', include(('testing.urls', 'testing'), namespace='testing')),
    ]
