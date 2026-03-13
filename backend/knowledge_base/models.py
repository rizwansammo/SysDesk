from django.conf import settings
from django.db import models
from django.utils.text import slugify

from core.mixins import TimeStampedModel
from organizations.models import Organization


class KnowledgeBaseArticle(TimeStampedModel):
    VISIBILITY_PUBLIC = "public"
    VISIBILITY_INTERNAL = "internal"

    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, "Public"),
        (VISIBILITY_INTERNAL, "Internal"),
    ]

    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="knowledge_base_articles",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    category = models.CharField(max_length=120, blank=True)
    content = models.TextField()
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_PUBLIC,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="kb_articles_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="kb_articles_updated",
    )
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "visibility"]),
            models.Index(fields=["organization"]),
            models.Index(fields=["category"]),
            models.Index(fields=["slug"]),
        ]
        unique_together = [("organization", "slug")]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title