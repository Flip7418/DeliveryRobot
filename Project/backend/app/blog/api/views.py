from django.db.models import Count
from django.http import Http404
from rest_framework import mixins, filters, status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from blog.api.serializers import ArticleRetrieveSerializer, \
    ArticleListSerializer, CommentCreateSerializer, ArticleLikeSerializer
from blog.models import Article, Comment
from blog.models.blog import ArticleLike
from core.paginations import SmallResultSetPagination


class ArticleOrderingFilterBackend(filters.BaseFilterBackend):
    """
    Custom ordering for articles list
    """
    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get('ordering', None)
        if ordering:
            if ordering in ["likes", "-likes"]:
                queryset = queryset.\
                    annotate(likes_count=Count('likes'))

                if "-" in ordering:
                    return queryset.order_by('-likes_count')
                else:
                    return queryset.order_by('likes_count')
            elif ordering in ['created_at', '-created_at']:
                queryset = queryset.order_by(ordering)
        return queryset


class ArticleViewSet(GenericViewSet, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ArticleRetrieveSerializer
    pagination_class = SmallResultSetPagination
    filter_backends = [filters.SearchFilter, ArticleOrderingFilterBackend]
    search_fields = ['title', 'author']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleRetrieveSerializer


class CommentViewSet(GenericViewSet, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentCreateSerializer


class ArticleLikeView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = ArticleLike.objects.all()
    serializer_class = ArticleLikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'article': self.kwargs['pk']})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class ArticleUnlikeView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = None

    def get_queryset(self):
        queryset = ArticleLike.objects.filter(user=self.request.user.id,
                                              article=self.kwargs['pk'])
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists():
            return queryset.first()
        else:
            raise Http404

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
