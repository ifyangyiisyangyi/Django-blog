# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


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
    return render(request, 'tool/commdty_code_make_up.html')


def sub_table(request):
    return render(request, 'tool/sub_table.html')
