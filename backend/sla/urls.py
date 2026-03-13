from django.urls import path

from .views import SLAListCreateView, SLARetrieveUpdateView

urlpatterns = [
    path("policies/", SLAListCreateView.as_view(), name="sla-list-create"),
    path("policies/<int:pk>/", SLARetrieveUpdateView.as_view(), name="sla-detail"),
]