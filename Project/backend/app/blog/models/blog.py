from django.db import models
from django.db.models import CASCADE

from user.models import User


class Article(models.Model):
    title = models.CharField(max_length=512)
    photo = models.ImageField()
    text = models.TextField()
    author = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "blog"
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=CASCADE,
                                related_name='likes')
    user = models.ForeignKey(User, on_delete=CASCADE,
                             related_name='likes')

    class Meta:
        app_label = "blog"
        verbose_name = "Article Like"
        verbose_name_plural = "Article likes"
