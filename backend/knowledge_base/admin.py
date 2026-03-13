from django.contrib import admin

from .models import KnowledgeBaseArticle


@admin.register(KnowledgeBaseArticle)
class KnowledgeBaseArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "organization",
        "category",
        "visibility",
        "status",
        "created_by",
        "published_at",
        "created_at",
    )
    list_filter = ("visibility", "status", "organization", "category")
    search_fields = ("title", "content", "slug", "category")
    readonly_fields = ("slug", "published_at", "created_at", "updated_at")