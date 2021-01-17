from django.shortcuts import render, redirect
from TestModel.models import User, UserForm


def show_404(request):
    return render(request, '404.html')


def index(request):
    pass
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(user_name=username)
                if user.password == password:
                    return redirect('/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    pass
    return render(request, 'register.html')


def logout(request):
    pass
    return render(request, 'logout.html')
