from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from .models import *


# функция представления главной страницы
def index(request):
    cats = Category.objects.all()
    posts = Review.objects.all()
    context = {
        'cats': cats,
        'posts': posts,
    }

    return render(request, 'reviews/index.html', context=context)


def show_post(request, post_id):
    return HttpResponse(f"отображение статьи с id={post_id}")


def show_category(request, cat_id):
    cats = Category.objects.all()
    posts = Review.objects.filter(cat_id=cat_id)

    if len(posts) == 0:
       raise Http404()

    context = {
        'cats': cats,
        'posts': posts,
    }
    return render(request, 'reviews/index.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')