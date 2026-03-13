from rest_framework import serializers

from organizations.models import Organization
from .models import KnowledgeBaseArticle


class KnowledgeBaseArticleListSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = KnowledgeBaseArticle
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "visibility",
            "status",
            "organization",
            "organization_name",
            "created_by",
            "created_by_name",
            "published_at",
            "created_at",
            "updated_at",
        ]


class KnowledgeBaseArticleDetailSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)
    updated_by_name = serializers.CharField(source="updated_by.full_name", read_only=True)

    class Meta:
        model = KnowledgeBaseArticle
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "content",
            "visibility",
            "status",
            "organization",
            "organization_name",
            "created_by",
            "created_by_name",
            "updated_by",
            "updated_by_name",
            "published_at",
            "created_at",
            "updated_at",
        ]


class KnowledgeBaseArticleCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=120, required=False, allow_blank=True)
    content = serializers.CharField()
    visibility = serializers.ChoiceField(choices=KnowledgeBaseArticle.VISIBILITY_CHOICES)
    status = serializers.ChoiceField(choices=KnowledgeBaseArticle.STATUS_CHOICES)
    organization = serializers.IntegerField(required=False, allow_null=True)

    def validate_organization(self, value):
        if value is None:
            return value
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected organization does not exist.")
        return value


class KnowledgeBaseArticleUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    category = serializers.CharField(max_length=120, required=False, allow_blank=True)
    content = serializers.CharField(required=False)
    visibility = serializers.ChoiceField(
        choices=KnowledgeBaseArticle.VISIBILITY_CHOICES,
        required=False,
    )
    status = serializers.ChoiceField(
        choices=KnowledgeBaseArticle.STATUS_CHOICES,
        required=False,
    )
    organization = serializers.IntegerField(required=False, allow_null=True)

    def validate_organization(self, value):
        if value is None:
            return value
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected organization does not exist.")
        return value