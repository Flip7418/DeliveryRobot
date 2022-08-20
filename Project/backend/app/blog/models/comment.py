from django.db import models
from django.db.models import CASCADE

from blog.models import Article
from user.models import User


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=CASCADE,
                                related_name='comments')
    user = models.ForeignKey(User, on_delete=CASCADE,
                             related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "blog"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at']
