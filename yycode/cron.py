import time

import requests
from django.core.mail import send_mail

from TestModel.models import Vistor


def send_email():
    res = send_mail('打卡提醒助手', "忙碌工作了一天，下班记得打卡哦~", '117645743@qq.com',
                    ['ifyangyiisyangyi@163.com', '937471204@qq.com', '506039913@qq.com'])
    print(res)


# 更新访问者信息
def update_vistor():
    vistor_list = Vistor.objects.filter(count=3, country='')
    for i in vistor_list:
        print(f'ip为 : {i.ip}')
        url = f"http://www.ip-api.com/json/{i.ip}?lang=zh-CN"
        try:
            res = requests.get(url, timeout=3)
            ip_message = res.json()
            print(ip_message)
            # now = time.strftime()  # todo 加了时间后会报错
            if ip_message.get('status') == 'success':
                i.country = ip_message.get('country')
                i.city = ip_message.get('city')
                i.ip_as = ip_message.get('as')
                i.isp = ip_message.get('isp')
                i.save()
                print("*******************保存成功******************")
            elif ip_message.get('status') == 'fail':
                print("请求失败")
            else:
                pass
        except:
            print("未知异常")
