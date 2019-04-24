from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .forms import CommentForm


def post_comment(request, post_pk):

    # 先获取被评论的文章，因为后面需要吧评论和被评论的文章关联起来
    # 这里我们使用了Django提供的一个快捷函数 get_onject_or_404
    # 这个函数的作用是获取的文章（Post）存在时；否则返回404页面给用户

    post = get_object_or_404(Post, pk=post_pk)

    # HTTP请求有get和post两种，一般用户通过表单提交数据都是通过post提交请求，
    # 因此只用当用户的请求为post是才需要处理数据
    if request.method == 'POST':
        # 用户提交的数据存在request.POST中，这是一个类字典
        # 我们利用这些数据构造CommentForm的实例，这样Django的表单就生成了
        form = CommentForm(request.POST)

        # 当调用form.is_valid()方法手，Django自动帮助我们检查表单的数据是否符合格式要求
        if form.is_valid():
            # 检查数据是合法的，调用表单的save方法保存数据到数据库中
            # commit=FALSE 的作用仅仅利用表单的数据生成Comment模型类的实例，但不保存数据到数据库
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来
            comment.post = post

            # 最终将评论数据保存进数据库，调用模型实例的save方法
            comment.save()

            # 重定向到post的详情页，实际上当redirect函数接收一个函数模型时，他会调用这个模型实例的get_absolute_url方法
            # 然后重定向到get_absolute_url 方法返回的URL
            return redirect(post)
        else:
            # 检查数据不合法， 重新渲染详情页，并且渲染表单的错误
            # 隐藏我们传了三个模板变量给detail.html
            # 一个是文章（Post），一个是评论列表，一个是表单form
            # 注意这里我们用到了post.comment_set.all()方法
            # 这个用法有点类似于Post。object().all()，作用是获取这篇文章post下的全部评论
            # 因为post和Comment是Foreignkey关联的，会因此使用post.comment_set.all()反向查询全部评论内容
            comment_list = post.comment_set.all()
            context = {

                'post': post,
                'form': form,
                'comment_list': comment_list
            }
    return render(request, 'blog/detail.html', context=context)

    # 不是post请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)







