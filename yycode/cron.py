import time

import requests
from django.core.mail import send_mail

from TestModel.models import Vistor


def send_email():
    res = send_mail('good afternoon my neighbour', "基友拍了拍我开始摇尾巴", '117645743@qq.com',
                    ['ifyangyiisyangyi@163.com'])
    print(res)


# 更新访问者信息
def update_vistor():
    vistor_list = Vistor.objects.filter(count=1, country='')
    for i in vistor_list:
        print(f'ip为 : {i.ip}')
        url = f"http://www.ip-api.com/json/{i.ip}?lang=zh-CN"
        res = requests.get(url)
        ip_message = res.json()
        print(ip_message)
        try:
            now = time.strftime()
            if ip_message.get('status') == 'success':
                i.country = ip_message.get('country')
                print(i.country)
                i.city = ip_message.get('city')
                print(i.city)
                i.ip_as = ip_message.get('as')
                print(i.ip_as)
                i.isp = ip_message.get('isp')
                print(i.isp)
                print("获取访问者信息成功")
                i.save()
                print(f"保存耗时{time.strftime() - now}")
            elif ip_message.get('status') == 'fail':
                print("请求失败")
            else:
                print("更新失败")
        except:
            print("未知异常")
