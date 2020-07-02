from django.shortcuts import render

from .models import Post, Comment
from .forms import CommentForm


def index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = { 'posts': posts }

    return render(request, 'blog/index.html', context)

def category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by('-created_on')
    context = {
        'category': category,
        'posts': posts
    }

    return render(request, 'blog/category.html', context)

def detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data['author'],
                body=form.cleaned_data['body'],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'blog/detail.html', context)
 