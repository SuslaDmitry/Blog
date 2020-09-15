from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Tag
from .forms import BlogPostForm, TagForm
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
import datetime


# Create your views here.
@login_required
def owner_posts(request):
    """Страница My posts приложения Blog выводит список постов владельца"""
    owner_posts = BlogPost.objects.filter(owner=request.user).order_by('-date_added')
    paginator = Paginator(owner_posts, 12)
    page_number = request.GET.get('page', 1)
    owner_page = paginator.get_page(page_number)

    if owner_page.has_next():
        next_url = f'?page={owner_page.next_page_number()}'
    else:
        next_url = ''
    if owner_page.has_previous():
        prev_url = f'?page={owner_page.previous_page_number()}'
    else:
        prev_url = ''

    context = {'owner_page': owner_page,
               'owner_posts': owner_posts,
               'next_owner_page_url': next_url,
               'prev_owner_page_url': prev_url}
    return render(request, 'blogs/my_posts.html', context)


def public_posts(request):
    """Выводит список публичных тем на главной странице"""
    public_posts = BlogPost.objects.filter(public=True).order_by('-date_added')
    paginator = Paginator(public_posts, 10)
    page_number = request.GET.get('page', 1)
    public_page = paginator.get_page(page_number)

    if public_page.has_next():
        next_url = f'?page={public_page.next_page_number()}'
    else:
        next_url = ''
    if public_page.has_previous():
        prev_url = f'?page={public_page.previous_page_number()}'
    else:
        prev_url = ''

    context = {'public_page': public_page,
               'public_posts': public_posts,
               'next_public_page_url': next_url,
               'prev_public_page_url': prev_url}
    return render(request, 'blogs/index.html', context)


@login_required
def new_post(request):
    """Добавляет новый пост."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = BlogPostForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            form.save_m2m()
            if new_post.public:
                return HttpResponseRedirect(reverse('blogs:index'))
            else:
                return HttpResponseRedirect(reverse('blogs:owner_posts'))
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """Редактирует существующий пост."""
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = BlogPostForm(instance=post)
    else:
        # Отправка данных POST; обработать данные.
        form = BlogPostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            post.date_edit = datetime.datetime.now()
            form.save()
        return HttpResponseRedirect(reverse('blogs:owner_posts'))

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


def post_details(request, post_id):
    """Выводит пост целиком"""
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user and post.public != True:
        raise Http404

    context = {'post': post}
    return render(request, 'blogs/post_details.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        raise Http404
    post.delete()
    return HttpResponseRedirect(reverse('blogs:owner_posts'))


@login_required
def privat_public(request, post_id):
    """Публикует/скрывает пост"""
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        raise Http404
    if post.public:
        post.public = False
    else:
        post.public = True
        post.date_publication = datetime.datetime.now()
    post.save()
    if post.public:
        return HttpResponseRedirect(reverse('blogs:index'))
    else:
        return HttpResponseRedirect(reverse('blogs:owner_posts'))


def tag_detail(request, tag_id):
    """Выводит список постов по заданому тегу"""
    tag = get_object_or_404(Tag, id=tag_id)
    tag_posts = tag.posts.all()
    paginator = Paginator(tag_posts, 10)
    page_number = request.GET.get('page', 1)
    tag_page = paginator.get_page(page_number)

    if tag_page.has_next():
        next_url = f'?page={tag_page.next_page_number()}'
    else:
        next_url = ''
    if tag_page.has_previous():
        prev_url = f'?page={tag_page.previous_page_number()}'
    else:
        prev_url = ''

    context = {'tag': tag,
               'tag_page': tag_page,
               'tag_posts': tag_posts,
               'next_tag_page_url': next_url,
               'prev_tag_page_url': prev_url}
    return render(request, 'blogs/tag_detail.html', context)


@login_required
def new_tag(request):
    """Добавляет новый пост."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = TagForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:new_tag'))
    context = {'form': form}
    return render(request, 'blogs/new_tag.html', context)


@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return HttpResponseRedirect(reverse('blogs:new_tag'))
