from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .forms import *
from .models import *


class ReviewHome(ListView):
    model = Review
    template_name = 'reviews/index.html'
    context_object_name = 'posts'  # что бы использовать в шаблоне posts а не object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            **kwargs)  # Здесь super() – это обращение к базовому классу и, далее, через точку, идет вызов аналогичного метода с передачей ему возможных именованных параметров из словаря kwargs. Сформированный базовый контекст мы сохраняем через переменную context.
        context['title'] = 'Главная страница'
        return context

    # функция отображает только опубликованные статьи
    def get_queryset(self):
        return Review.objects.filter(is_published=True).order_by('-time_create')


class ShowPost(FormMixin, DetailView):
    model = Review
    template_name = 'reviews/post.html'
    slug_url_kwarg = 'post_slug'  # Без этого в URL post/<slug:slug>/
    context_object_name = 'post'
    form_class = CommentForm

    success_url = reverse_lazy('home')

    # переопределяю что бы отаться на стр post/slug
    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('post', kwargs={'slug': self.get_object().slug})

    # Переопределение для правильной работы формы комменнтарие
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.review = self.get_object()  # то что передаем
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)



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


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm  # указываем класс формы
    template_name = 'reviews/addpage.html'
    success_url = reverse_lazy('home')
    prepopulated_fields = {"slug": ("title",)}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)  # метод сохранения пока не вызван
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class AdminPanel(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews/adminpage.html'
    form_class = AddPostForm
    success_url = reverse_lazy('admin_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['post_list'] = Review.objects.all().order_by('id')
        return context


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = AddPostForm
    template_name = 'reviews/updatepost.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование статьи'
        context['post_list'] = Review.objects.all().order_by('id')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/deletepage.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    success_url = "/adminpage/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


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
    # post_reset_login_backend = 'django.contrib.auth.backends.ModelBackend'
    form_class = LoginUserForm
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
