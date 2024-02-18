import datetime
import hashlib

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect

from TestModel import models
from TestModel.models import User
from TestModel.forms import UserForm, RegisterForm
from blog.views import log
from yycode import settings


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
                if user.has_confirmed == False:
                    message = "用户还未邮件确认"
                    return render(request, 'login.html', locals())
                if user.password == md5_code(password):
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
    if request.session.get('is_login', None):
        return redirect('/')
    if request.method == "POST":
        log.debug('--> post')
        register_form = RegisterForm(request.POST)
        # log.info(register_form)
        message = '请检查填写的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不同'
                return render(request, 'register.html', locals())
            else:
                same_username = User.objects.filter(user_name=username)
                if same_username:
                    message = "用户名已存在"
                    return render(request, 'register.html', locals())
                same_mail = User.objects.filter(email=email)
                if same_mail:
                    message = "邮箱已存在"
                    return render(request, 'register.html', locals())
                new_user = User(
                    user_name=username,
                    password=md5_code(password1),  # 使用md5加密
                    email=email,
                    sex=sex
                )
                new_user.save()
                code = make_confirm_string(new_user)
                send_register_mail(email, code)
                message = "请前往注册邮箱，进行邮件确认"
                return render(request, 'confirm.html', locals())  # 跳到邮件确认页
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


# 登出
def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')


# 密码md5加密
def md5_code(s, salt='md5'):
    s = (str(s) + salt).encode()
    m = hashlib.md5(s)
    return m.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = md5_code(user.user_name, salt=now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


# 发送注册邮件
def send_register_mail(email, code):
    subject, from_email = '账号注册确认邮件', '117645743@qq.com'
    text_content = '欢迎注册'
    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>点击确认</a></p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('yycode.com.cn', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# 注册邮件确认
def user_confirm(request):
    code = request.GET.get('code', None)
    print(f'code --> {code}')
    message = ""
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())
    create_time = confirm.create_time
    now = datetime.datetime.now()
    if now > create_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', locals())


