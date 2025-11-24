from django.shortcuts import render, get_object_or_404  # type: ignore[import]
from django.utils import timezone  # type: ignore[import]
from .models import Post, Category


def index(request):
    """
    Главная страница с пятью последними публикациями.
    Выводит только опубликованные посты с датой не позже текущего времени.
    """
    post_list = (
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
        .select_related('category', 'location', 'author')
        .order_by('-pub_date')[:5]
    )

    context = {
        'posts': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """
    Страница отдельного поста.
    Показывает только опубликованные посты с датой не позже текущего времени.
    """
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ).select_related('category', 'location', 'author'),
        pk=post_id,
    )

    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """
    Страница с постами определенной категории.
    Показывает только опубликованные посты с датой не позже текущего времени.
    """
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    post_list = (
        Post.objects.filter(
            category=category,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
        .select_related('category', 'location', 'author')
        .order_by('-pub_date')
    )

    context = {
        'posts': post_list,
        'category_slug': category_slug
    }
    return render(request, 'blog/category.html', context)
