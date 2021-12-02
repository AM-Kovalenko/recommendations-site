from django.conf.urls import url
from django.urls import path, re_path, include
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
    url('', include('social_django.urls', namespace='social')),
    path('accounts/profile/', LoginUser.as_view(), name='login_github'),
    path('login/google-oauth2/', LoginUser.as_view(), name='login_google'),
]