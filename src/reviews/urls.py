from django.urls import path, re_path
from .views import *


urlpatterns = [
    # path('', index, name='home'),                #http://127.0.0.1:8000/
    # path('post/<int:post_id>/', show_post, name='post'),
    # path('category/<int:cat_id>/', show_category, name='category'),
    # path('addpage/', addpage, name='add_page'),
    path('', ReviewHome.as_view(), name='home'),    # Это метод одного из базовых классов вида и служит для привязки класса представления к текущему маршруту.
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>', ReviewCategory.as_view(), name='category'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

    # path('', WomenHome.as_view(), name='home'),  # Это метод одного из базовых классов вида и служит для привязки класса представления к текущему маршруту.
    # path('about/', about, name='about'),
    # # path('addpage/', addpage, name='add_page'),
    # path('addpage/',AddPage.as_view(), name='add_page'),
    # path('contact/', contact, name='contact'),
    # path('login/', login, name='login'),
    # path('post/<slug:post_slug>/', show_post, name='post'),
    # path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # # path('category/<int:cat_id>/', show_category, name='category')
    # path('category/<slug:cat_slug>', WomenCategory.as_view(), name='category')
]