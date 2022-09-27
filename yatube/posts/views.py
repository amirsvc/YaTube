from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User

from yatube.settings import QUANTITY


@cache_page(20, key_prefix='index_page')
def index(request):
    template = "posts/index.html"
    title = "Последние обновления на сайте"
    posts = Post.objects.all()
    paginator = Paginator(posts, QUANTITY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "title": title,
    }
    return render(request, template, context)


def group_posts(request, any_slug):
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=any_slug)
    title = group
    posts = group.groups_name.all()
    paginator = Paginator(posts, QUANTITY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj": page_obj,
        "title": title,
    }
    return render(request, template, context)


def profile(request, username):
    template = "posts/profile.html"
    user = get_object_or_404(User, username=username)
    title = f"Профайл пользователя {username}"
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, QUANTITY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=user
    ).exists()
    context = {
        "author": user,
        "page_obj": page_obj,
        "title": title,
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = "posts/post_detail.html"
    post_item = get_object_or_404(Post, pk=post_id)
    title = f'Пост { post_item.text[0:30] }'
    form = CommentForm(request.POST or None)
    comment = post_item.comments.all()
    context = {
        "post_item": post_item,
        "title": title,
        "form": form,
        "comments": comment
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = "posts/create.html"
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    template = "posts/create.html"
    form = PostForm()
    context = {
        "form": form
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post_item = get_object_or_404(Post, pk=post_id, author=request.user)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post_item
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_item.id)
    form = PostForm(instance=post_item)
    template = "posts/create.html"
    context = {
        "post_item": post_item,
        "form": form,
        "is_edit": True
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, QUANTITY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        Follow.objects.get_or_create(
            user=user,
            author=author
        )
        return redirect('posts:follow_index')
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    unfollow = get_object_or_404(User, username=username)
    follow = request.user.follower.filter(author=unfollow)
    if follow.exists():
        follow.delete()
    return redirect('posts:profile', username)
