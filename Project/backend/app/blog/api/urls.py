from django.urls import path, include
from rest_framework import routers

from blog.api.views import ArticleViewSet, CommentViewSet, ArticleLikeView, \
    ArticleUnlikeView

router = routers.DefaultRouter()
router.register(r"article", ArticleViewSet, basename="articles")
router.register(r"comment", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
    path('article/<int:pk>/like/', ArticleLikeView.as_view(),
         name='article_like'),
    path('article/<int:pk>/unlike/', ArticleUnlikeView.as_view(), name='article_unlike'),
]
