from .views import index, change_theme
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("switch/", change_theme, name="change_theme"),
    path("", index, name='index'),
    path("", include('users.urls')),
    path("", include('status.urls')),
]

if settings.DEBUG:
    # print("*"*50)
    # print(f"DEBUG: {settings.DEBUG}")
    # print("*"*50)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls"))
    ]
