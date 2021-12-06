from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import *


# # функция представления главной страницы
# def index(request):
#     cats = Category.objects.all()
#     posts = Review.objects.all()
#     context = {
#         'cats': cats,
#         'posts': posts,
#         'title': 'Главная страница',
#     }
#     return render(request, 'reviews/index.html', context=context)
# ---------------------------------------------------------------------------
class ReviewHome(ListView):
    model = Review
    template_name = 'reviews/index.html'
    context_object_name = 'posts'  # что бы использовать в шаблоне posts а не object_list

    # педача динамических данных (списка menu) шаблону index.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            **kwargs)  # Здесь super() – это обращение к базовому классу и, далее, через точку, идет вызов аналогичного метода с передачей ему возможных именованных параметров из словаря kwargs. Сформированный базовый контекст мы сохраняем через переменную context.
        context['title'] = 'Главная страница'

        # c_def = self.get_user_context(title='Главная страница')
        # return dict(list(context.items()) + list(c_def.items()))
        return context

    # функция отображает только опубликованные статьи
    def get_queryset(self):
        return Review.objects.filter(is_published=True).order_by('-time_create')


# ------------------------------------------------------------------------------
# def show_post(request, post_slug):
#     post = get_object_or_404(Review, slug=post_slug)
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'reviews/post.html', context=context)

class ShowPost(DetailView):
    model = Review
    template_name = 'reviews/post.html'
    slug_url_kwarg = 'post_slug'  # Без этого в URL post/<slug:slug>/
    context_object_name = 'post'


# ----------------------------------------------------------------------------------------
# def show_category(request, cat_id):
#     cats = Category.objects.all()
#     posts = Review.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'cats': cats,
#         'posts': posts,
#         'title': 'Главная страница',
#     }
#     return render(request, 'reviews/index.html', context=context)


class ReviewCategory(ListView):
    model = Review
    template_name = 'reviews/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Review.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context


# -----------------------------------------------------------------------

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST)
#         if form.is_valid():
#             try:
#                 Review.objects.create(**form.cleaned_data)
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#
#     context = {
#         'form': form,
#         'title': 'Добавление страницы'
#     }
#     return render(request, 'reviews/addpage.html', context=context)

class AddPage(CreateView):
    form_class = AddPostForm  # указываем класс формы
    template_name = 'reviews/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        # import pdb;pdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context


def adminpage(request):
    cats = Category.objects.all()
    post_list = Review.objects.all().order_by('id')
    context = {
        'cats': cats,
        'title': 'Админ панель',
        'post_list': post_list
    }
    return render(request, 'reviews/adminpage.html', context=context)


class UpdatePost(UpdateView):
    model = Review
    form_class = AddPostForm
    template_name = 'reviews/updatepost.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


class DeletePost(DeleteView):
    model = Review
    template_name = 'reviews/deletepage.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    success_url = "/adminpage/"


# ------------------------------------------------------------------------------
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(CreateView):
    form_class = RegisterUserForm  # Использую собственную форму вместо UserCreationForm
    template_name = 'reviews/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'reviews/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
