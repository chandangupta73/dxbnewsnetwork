from django.shortcuts import render

def Generalist_Sign_Up(request):
    return render(request, 'inn/generalist_sign_up.html')


def Generalist_SignIn(request):
    return render(request, 'inn/generalist_registration.html')


def Generalist_Forgot_Password(request):
    return render(request, 'inn/generalist_forgot_password.html')


def Generalist_New_Password(request):
    return render(request, 'inn/generalist_new_password.html')


def Generalist_Dashboard(request):
    return render(request, 'inn/generalist_dashboard.html')


def Generalist_Profile(request):
    return render(request, 'inn/generalist_profile.html')


def Generalist_Update_Profile(request):
    return render(request, 'inn/generalist_update_profile.html')


def Generalist_News_Post(request):
    return render(request, 'inn/generalist_news_post.html')


def Generalist_Manage_Post(request):
    return render(request, 'inn/generalist_manage_post.html')


def Generalist_Edit_News_Post(request):
    return render(request, 'inn/generalist_edit_news_Post.html')
