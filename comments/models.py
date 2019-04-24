

from django.db import models
from django.utils.six import python_2_unicode_compatible


# python_2_unicode_compatible 装饰器用于兼容Python2
@python_2_unicode_compatible
class Comment(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post',on_delete=models.CASCADE)

    def __str__(self):
        self.text[:20]

    class Meta(object):
        verbose_name = '评论'
        verbose_name_plural = '评论'

