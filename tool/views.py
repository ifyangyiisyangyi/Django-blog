# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from tool.models import Linkage


def Toolview(request):
    return render(request, 'tool/tool.html')


class Cbvdemo(View):
    context = {
        'code': 0,
        'msg': ''
    }

    def get(self, request):
        self.context['msg'] = '这是Cbvdemo get请求'
        return JsonResponse(self.context)

    def post(self, request):
        self.context['msg'] = '这是Cbvdemo post请求'
        return JsonResponse(self.context)


def commdty_code_make_up(request):
    '''
    商品编码补齐
    '''
    return render(request, 'tool/commdty_code_make_up.html')


def sub_table(request):
    '''
    查询分表
    '''
    return render(request, 'tool/sub_table.html')


def mock(request):
    '''
    在线mock工具
    '''
    # print(f'**********   {request.method}   **********')
    # if request.method == 'POST':
    #     return render(request, 'tool/mock.html', context={'mockUrl': 'xxx/xxx'})
    return render(request, 'tool/mock.html')


def link_show(request):
    '''
    常用链接
    '''
    linkages = Linkage.objects.all()
    return render(request, 'tool/link_show.html', {'linkages': linkages})
