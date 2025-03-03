from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.Generalist_Sign_Up, name='sign-up'),
    path('sign-in/', views.Generalist_SignIn, name='sign-in'),
    path('forgot-password/', views.Generalist_Forgot_Password, name='forgot-password'),
    path('new-password/', views.Generalist_New_Password, name='new-password'),
    path('dashboard/', views.Generalist_Dashboard, name='dashboard'),
    path('profile/', views.Generalist_Profile, name='profile'),
    path('update-profile/', views.Generalist_Update_Profile, name='update-profile'),
    path('news-post/', views.Generalist_News_Post, name='news-post'),
    path('news-post/', views.Generalist_News_Post, name='news-post'),
    path('manage-post/', views.Generalist_Manage_Post, name='manage-post'),
    path('edit-news-post/', views.Generalist_Edit_News_Post, name='edit-news-post'),
]
