from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

admin.site.site_header = "SysDesk Helpdesk"
admin.site.site_title = "SysDesk Helpdesk Admin"
admin.site.index_title = "Welcome to SysDesk Helpdesk"

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/v1/tickets/", include("tickets.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)