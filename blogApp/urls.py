from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('post/<str:slug>', detail, name='details'),
    path('contact', contact_view, name='contact'),
    path('about', About, name='about'),
    path('register', register, name='register'),

    path('login/', login, name='login'),
    path('logout', logout, name='logout'),
    path('dashboard',dashboard, name='dashboard'),
    # path('password_reset', forgotpwd, name='forgotPassword'),
    # path('reset_password/<uidb64>/<token>', reset_password, name='reset_password'),
    path('new-post', newpost.as_view(), name='newpost'),
    path('edit-post/<str:slug>', editpost.as_view(), name='editpost'),
    path('delete-post/<str:slug>/', delete_post, name='delete_post'),
]