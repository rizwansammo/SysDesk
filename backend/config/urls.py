from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import AgentListView, MeView, UserListCreateView, UserRetrieveUpdateView

admin.site.site_header = "SysDesk Helpdesk"
admin.site.site_title = "SysDesk Helpdesk Admin"
admin.site.index_title = "Welcome to SysDesk Helpdesk"

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/auth/me/", MeView.as_view(), name="auth-me"),

    path("api/v1/users/", UserListCreateView.as_view(), name="users-list-create"),
    path("api/v1/users/<int:pk>/", UserRetrieveUpdateView.as_view(), name="users-detail"),
    path("api/v1/agents/", AgentListView.as_view(), name="agents-list"),

    path("api/v1/tickets/", include("tickets.urls")),
    path("api/v1/organizations/", include("organizations.urls")),
    path("api/v1/knowledge-base/", include("knowledge_base.urls")),
    path("api/v1/sla/", include("sla.urls")),
    path("api/v1/automation/", include("automation.urls")),
    path("api/v1/audit/", include("audit.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)