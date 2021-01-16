from django.shortcuts import render, redirect
from TestModel.models import User


def show_404(request):
    return render(request, '404.html')


def index(request):
    pass
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        user_name = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(user_name)
        if user_name and password:  # 确保用户名和密码都不为空
            user_name = user_name.strip()
            try:
                user = User.objects.get(user_name=user_name)
            except:
                return render(request, 'login.html')
            if user.password == password:
                return redirect('/')
    return render(request, 'login.html')


def register(request):
    pass
    return render(request, 'register.html')


def logout(request):
    pass
    return render(request, 'logout.html')
