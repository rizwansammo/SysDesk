from django.urls import path

from .views import (
    KnowledgeBaseArticleListCreateView,
    KnowledgeBaseArticleRetrieveUpdateView,
    KnowledgeBaseSearchView,
)

urlpatterns = [
    path("articles/", KnowledgeBaseArticleListCreateView.as_view(), name="kb-article-list-create"),
    path("articles/<int:pk>/", KnowledgeBaseArticleRetrieveUpdateView.as_view(), name="kb-article-detail"),
    path("search/", KnowledgeBaseSearchView.as_view(), name="kb-search"),
]