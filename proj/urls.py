
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
    path('dj-admin/', admin.site.urls),
    path('',include('employee.urls')),
    path('admin/',include('customadmin.urls')),
    path('client/',include('client.urls')),
    path('chat/',include('chat.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)