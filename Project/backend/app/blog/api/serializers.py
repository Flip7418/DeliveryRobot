from django.shortcuts import get_object_or_404
from rest_framework import serializers

from blog.models import Article, Comment
from blog.models.blog import ArticleLike


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'article')

    def validate(self, attrs):
        attrs['user'] = self.context["request"].user
        return attrs


class CommentRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at')

    def get_author(self, comment):
        full_name = f"{comment.user.first_name} {comment.user.last_name}"
        full_name = full_name.strip()

        if full_name == "":
            full_name = comment.user.sdu_id

        return full_name


class ArticleListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'photo', 'text', 'author', 'created_at',
                  'likes_count', 'comments_count')

    def get_likes_count(self, article):
        return article.likes.count()

    def get_comments_count(self, article):
        return article.comments.count()


class ArticleRetrieveSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    comments = CommentRetrieveSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'photo', 'text', 'author', 'created_at',
                  'is_liked', 'comments')

    def get_is_liked(self, article):
        user = self.context["request"].user

        return article.likes.filter(user=user.id).exists()


class ArticleLikeSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ArticleLike
        fields = ('article', )

    def validate(self, attrs):
        article = get_object_or_404(Article, pk=self.initial_data[
            'article'])
        attrs['article'] = article
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        article_like, _ = ArticleLike.objects.get_or_create(
            user_id=validated_data['user'].id, article_id=validated_data[
                'article'].id)
        return article_like
