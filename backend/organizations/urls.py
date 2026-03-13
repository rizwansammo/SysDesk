from django.urls import path

from .views import OrganizationListCreateView, OrganizationRetrieveUpdateView

urlpatterns = [
    path("", OrganizationListCreateView.as_view(), name="organizations-list-create"),
    path("<int:pk>/", OrganizationRetrieveUpdateView.as_view(), name="organizations-detail"),
]