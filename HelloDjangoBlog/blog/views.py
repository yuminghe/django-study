import re

import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView
from .models import Post, Category, Tag


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify)
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


class ArchiveView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return super(ArchiveView, self).get_queryset().filter(
            create_time__year=year,
            create_time__month=month
        ).order_by('-create_time')

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        """父类的 get_queryset 方法。该方法默认获取指定模型的全部列表数据"""
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagyView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        """父类的 get_queryset 方法。该方法默认获取指定模型的全部列表数据"""
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagyView, self).get_queryset().filter(tag=t).order_by('-create_time')
