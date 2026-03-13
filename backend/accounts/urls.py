from django.urls import path

from .views import AgentListView, MeView, UserListCreateView, UserRetrieveUpdateView

urlpatterns = [
    path("me/", MeView.as_view(), name="auth-me"),
    path("users/", UserListCreateView.as_view(), name="users-list-create"),
    path("users/<int:pk>/", UserRetrieveUpdateView.as_view(), name="users-detail"),
    path("agents/", AgentListView.as_view(), name="agents-list"),
]