

from .models import Post, Category
from django.shortcuts import render, get_object_or_404
import markdown
from comments.forms import CommentForm


# 首页
def index(request):

    post_list = Post.objects.all().order_by('-create_time')

    return render(request, 'blog/index.html', context= {'post_list' : post_list})


# 详情
def detail(request, pk):

    post = get_object_or_404(Post, pk=pk)

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    form  = CommentForm()
    # 获取这篇文章post下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表达、以及文章下的评论列表作为模板能量传递给detail.html模板，以便进行相应的渲染
    context = {
        'post' : post,
        'form' : form,
        'comment_list' : comment_list
    }

    return render(request, 'blog/detail.html', context=context)


# 归档
def archives(request, year, month):

    post_list = Post.objects.filter(
                create_time__year=year,
                create_time__month=month
    ).order_by('-create_time')

    return render(request, 'blog/index.html', context={'post_list' : post_list})


# 分页
def category(request, pk):

    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list' : post_list})
