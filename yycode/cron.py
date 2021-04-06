import re
import requests
from django.core.mail import send_mail
from TestModel.models import Vistor
from blog.views import log


# def daily_reminder():
#     '''
#     周一至周五日报提醒
#     '''
#     html = '''
#         <!DOCTYPE HTML>
#         <html>
#         <head>
#             <meta charset="UTF-8">
#             <title>日报提醒</title>
#         </head>
#         <body>
#             <div>
#             <h1>写日报了咩?</h1>
#             </div>
#         </body>
#         </html>
#         '''
#     send_mail('日报提醒', '写日报了咩？', '117645743@qq.com', ['937471204@qq.com'], fail_silently=False, html_message=html)


def send_weather():
    """
    周一至周五上下班打卡提醒
    """
    weather_url = f'https://tianqiapi.com/api?version=v6&cityid=101010100&appid=62884591&appsecret=RktG3jTx'
    weather = requests.get(weather_url, timeout=5).json()
    city = weather['city']  # 城市
    wea = weather['wea']  # 天气情况
    tem = weather['tem']  # 平均气温
    tem1 = weather['tem1']  # 最高气温
    tem2 = weather['tem2']  # 最低气温
    win = weather['win']  # 风向
    win_speed = weather['win_speed']  # 风力等级
    win_meter = weather['win_meter']  # 风速
    air_level = weather['air_level']  # 空气质量
    air_tips = weather['air_tips']  # tips
    h = f'''
        <!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>天气订阅</title>
        </head>
        <body>
            <img src="https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1846888102,1087843010&fm=26&gp=0.jpg" height=150 width=300/></p>
            城市: {city} <br>
            天气情况: {wea} <br>
            平均气温: {tem}℃ <br>
            最高气温: {tem1}℃ <br>
            最低气温: {tem2}℃ <br>
            风向: {win} <br>
            风力等级: {win_speed} <br>
            风速: {win_meter} <br>
            空气质量: {air_level} <br>
            tips: {air_tips} <br>
        </body>
        </html>
        '''
    send_mail('打卡提醒', 'message', '117645743@qq.com', ['506039913@qq.com'], fail_silently=False,
              html_message=h)


# 更新访问者信息
def update_vistor():
    vistor_list = Vistor.objects.filter(count=3, country='')
    for i in vistor_list:
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                    i.ip):
            url = f"http://www.ip-api.com/json/{i.ip}?lang=zh-CN"
            res = requests.get(url, timeout=5)
            ip_message = res.json()
            log.info(f'解析IP响应结果 --> {ip_message}')
            if ip_message.get('status') == 'success':
                i.country = ip_message.get('country')
                i.city = ip_message.get('city')
                i.ip_as = ip_message.get('as')
                i.isp = ip_message.get('isp')
                i.save()
            elif ip_message.get('status') == 'fail':
                log.error(f"IP解析失败 --> {i.ip}")
            else:
                log.error(f'解析异常 --> {i.ip}')
        else:
            log.error(f'无法解析异常IP --> {i.ip}')
