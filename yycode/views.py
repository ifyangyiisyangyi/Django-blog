from django.shortcuts import render, redirect
from TestModel.models import User
from TestModel.forms import UserForm
from blog.views import log


def show_404(request):
    return render(request, '404.html')


# 登录
def login(request):
    # 不允许重复登录
    res = request.session.get('is_login')
    log.debug(f'request session  --> {res}')
    if request.session.get('is_login', None):
        return redirect('/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(user_name=username)
                if user.password == password:
                    # 往session字典内写入用户状态和数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.user_name
                    log.info(request.session['user_name'])
                    return redirect('/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
    '''
    这里使用了一个小技巧，Python内置了一个locals()函数，它返回当前所有的本地变量字典，
    我们可以偷懒的将这作为render函数的数据字典参数值，就不用费劲去构造一个形如
    {'message':message, 'login_form':login_form}的字典了。
    这样做的好处当然是大大方便了我们，但是同时也可能往模板传入了一些多余的变量数据，造成数据冗余降低效率
    '''
    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    pass
    return render(request, 'register.html')


# 登出
def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')