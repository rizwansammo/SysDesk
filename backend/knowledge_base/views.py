from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSupportStaff
from organizations.models import Organization
from .models import KnowledgeBaseArticle
from .serializers import (
    KnowledgeBaseArticleCreateSerializer,
    KnowledgeBaseArticleDetailSerializer,
    KnowledgeBaseArticleListSerializer,
    KnowledgeBaseArticleUpdateSerializer,
)


class KnowledgeBaseArticleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = KnowledgeBaseArticle.objects.select_related(
            "organization",
            "created_by",
            "updated_by",
        ).all()

        user = request.user

        if user.role.code in ["super_admin", "agent"]:
            return queryset

        return queryset.filter(
            visibility=KnowledgeBaseArticle.VISIBILITY_PUBLIC,
            status=KnowledgeBaseArticle.STATUS_PUBLISHED,
        )

    def get(self, request):
        queryset = self.get_queryset(request)

        organization_id = request.query_params.get("organization")
        category = request.query_params.get("category")
        visibility = request.query_params.get("visibility")
        status_value = request.query_params.get("status")

        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        if category:
            queryset = queryset.filter(category__iexact=category)
        if visibility and request.user.role.code in ["super_admin", "agent"]:
            queryset = queryset.filter(visibility=visibility)
        if status_value and request.user.role.code in ["super_admin", "agent"]:
            queryset = queryset.filter(status=status_value)

        serializer = KnowledgeBaseArticleListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role.code not in ["super_admin", "agent"]:
            return Response(
                {"detail": "Only support staff can create knowledge base articles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = KnowledgeBaseArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = None
        organization_id = serializer.validated_data.get("organization")
        if organization_id is not None:
            organization = get_object_or_404(Organization, id=organization_id)

        status_value = serializer.validated_data["status"]

        article = KnowledgeBaseArticle.objects.create(
            title=serializer.validated_data["title"],
            category=serializer.validated_data.get("category", ""),
            content=serializer.validated_data["content"],
            visibility=serializer.validated_data["visibility"],
            status=status_value,
            organization=organization,
            created_by=request.user,
            updated_by=request.user,
            published_at=timezone.now() if status_value == KnowledgeBaseArticle.STATUS_PUBLISHED else None,
        )

        return Response(
            KnowledgeBaseArticleDetailSerializer(article).data,
            status=status.HTTP_201_CREATED,
        )


class KnowledgeBaseArticleRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = KnowledgeBaseArticle.objects.select_related(
            "organization",
            "created_by",
            "updated_by",
        ).all()

        if request.user.role.code in ["super_admin", "agent"]:
            return queryset

        return queryset.filter(
            visibility=KnowledgeBaseArticle.VISIBILITY_PUBLIC,
            status=KnowledgeBaseArticle.STATUS_PUBLISHED,
        )

    def get_object(self, request, pk):
        return get_object_or_404(self.get_queryset(request), pk=pk)

    def get(self, request, pk):
        article = self.get_object(request, pk)
        return Response(KnowledgeBaseArticleDetailSerializer(article).data)

    def patch(self, request, pk):
        if request.user.role.code not in ["super_admin", "agent"]:
            return Response(
                {"detail": "Only support staff can update knowledge base articles."},
                status=status.HTTP_403_FORBIDDEN,
            )

        article = get_object_or_404(KnowledgeBaseArticle, pk=pk)

        serializer = KnowledgeBaseArticleUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "title" in data:
            article.title = data["title"]
            article.slug = ""
        if "category" in data:
            article.category = data["category"]
        if "content" in data:
            article.content = data["content"]
        if "visibility" in data:
            article.visibility = data["visibility"]
        if "organization" in data:
            if data["organization"] is None:
                article.organization = None
            else:
                article.organization = get_object_or_404(Organization, id=data["organization"])
        if "status" in data:
            article.status = data["status"]
            if data["status"] == KnowledgeBaseArticle.STATUS_PUBLISHED and article.published_at is None:
                article.published_at = timezone.now()
            elif data["status"] != KnowledgeBaseArticle.STATUS_PUBLISHED:
                article.published_at = None

        article.updated_by = request.user
        article.save()

        return Response(KnowledgeBaseArticleDetailSerializer(article).data)


class KnowledgeBaseSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        queryset = KnowledgeBaseArticle.objects.select_related(
            "organization",
            "created_by",
            "updated_by",
        ).all()

        if request.user.role.code not in ["super_admin", "agent"]:
            queryset = queryset.filter(
                visibility=KnowledgeBaseArticle.VISIBILITY_PUBLIC,
                status=KnowledgeBaseArticle.STATUS_PUBLISHED,
            )

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(category__icontains=query)
            )

        serializer = KnowledgeBaseArticleListSerializer(queryset, many=True)
        return Response(serializer.data)


from django.shortcuts import render

# Create your views here.
