from django.urls import path

from .views import AutomationRuleListCreateView, AutomationRuleRetrieveUpdateView

urlpatterns = [
    path("rules/", AutomationRuleListCreateView.as_view(), name="automation-rule-list-create"),
    path("rules/<int:pk>/", AutomationRuleRetrieveUpdateView.as_view(), name="automation-rule-detail"),
]