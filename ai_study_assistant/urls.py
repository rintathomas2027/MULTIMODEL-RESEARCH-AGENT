from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from assistant.views import FrontendAppView

urlpatterns = [
    path('', FrontendAppView.as_view(), name='app_home'),
    path('admin/', admin.site.urls),
    
    # Support both with and without /api/ prefix for seamless routing
    path('api/auth/', include('users.urls')),
    path('api/', include('assistant.urls')),
    path('auth/', include('users.urls')),
    path('', include('assistant.urls')),
    
    # Serve uploaded media files (PDFs, DOCX, etc.) in production on Render
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
