from django.contrib import admin

from blog.models import Comment
from blog.models.blog import ArticleLike, Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleLike)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class ArticleAdmin(admin.ModelAdmin):
    pass
