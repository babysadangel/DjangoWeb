# -*- coding:utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible


# 分类
class Category(models.Model):

    name = models.CharField(max_length=100,verbose_name='分类')

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = '分类'
        verbose_name_plural = '分类'


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签')

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = '标签'
        verbose_name_plural = '标签'


# 文章
@python_2_unicode_compatible
class Post(models.Model):

    # 文章标题
    title = models.CharField(max_length=70, verbose_name='标题')

    # 文章正文
    body = models.TextField(verbose_name='文章正文')

    # 这两个列分别表示文章的创建时间和最后一次修改的时间，

    create_time = models.DateTimeField(verbose_name='创建时间')
    modifed_time = models.DateTimeField(verbose_name='修改时间')

    # 文章的摘要，可以没有文章的的摘要，但是默认情况下Charfield要求必须填入数据，否则会报错
    # 指定'Charfield' 的blank=True 设置这个值只有就可以允许为空值了

    excerpt = models.CharField(max_length=200, blank=True , verbose_name='摘要')

    # 这是分类与标签，分类与标签的模型在上面已经定义
    # 我么这里要把文章对应的数据库和分类、标签对应的数据库表关联起来
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章。所以我们使用的是Foreignkey,既一对多的关系
    # 而对于标签来说，一篇文章可以有多个标签，同一标签下也可能有多篇文章，所以我们使用ManyToManyFeild，这表明是多对多的关系
    # 同时我们规定文章可以没有标签，因此标签tag指定了blank=True on_其中delete=models.CASCADE 在Django2.0中一定要填写

    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name='分类')
    tag = models.ManyToManyField(Tag,blank=True)

    # 文章作者，这里直接使用Django中django.contrib.auth.mddels，这个Django中内置的应用，专门处理用户注册登录流程
    # 这我们通过Foreignkey把文章和User关联起来
    # 因为一篇文章只能有一个作则，而一个作者可能会写多篇文章，因此这是一个一对多的关系，和category像类似
    author = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta(object):
        verbose_name = '文章'
        verbose_name_plural='文章'
        ordering = ['-create_time']
