from django.conf.urls import url
from django.urls import path, re_path, include
from .views import *


urlpatterns = [
    path('', ReviewHome.as_view(), name='home'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>', ReviewCategory.as_view(), name='category'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    url('', include('social_django.urls', namespace='social')),
    path('accounts/profile/', LoginUser.as_view(), name='login_github'),
    path('login/google-oauth2/', LoginUser.as_view(), name='login_google'),
    path('adminpage/', AdminPanel.as_view(), name='admin_page'),
    path('updatepost/<slug:post_slug>/', UpdatePost.as_view(), name='updatepost'),
    path('deletepost/<slug:post_slug>/', DeletePost.as_view(), name='deletepost'),
]