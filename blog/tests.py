from django.test import TestCase

# Create your tests here.
from TestModel.models import Vistor


class VistorTestCase(TestCase):
    """
    def setUp(self)：用来初始化环境，包括创建初始数据，或做一些其他准备工作
    def test_xxx(self)：xxx可以是任何东西，以test_开头的方法，都会被django认为是需要测试的方法，跑测试时会被执行。
        注：每个需要被测试的方法都是相互独立的
    def tearDown(self)：跟setUp相对，用来清理测试环境和测试数据（在django中可以不关心这个）
    """

    def setUp(self):
        print("setUp")
        Vistor.objects.create(
            ip='223.70.230.166',
            user_agent='',
            count='1',
            city='',
            country='',
            ip_as='',
            isp=''
        )
        Vistor.objects.create(
            ip='223.70.230.111',
            user_agent='',
            count='1',
            city='',
            country='',
            ip_as='',
            isp=''
        )
        Vistor.objects.create(
            ip='223.70.230.111',
            user_agent='',
            count='0',
            city='',
            country='',
            ip_as='',
            isp=''
        )

    def test_filter(self):
        print('test_filter')
        vistor = Vistor.objects.filter(count=1, user_agent = '')
        print(f':{vistor}')
        for i in vistor:
            print(i)
            print(i.ip)
            i.country = 'cn'
            i.city = 'bj'
            i.save()
            print(i.city)
        print(Vistor.objects.filter(city='bj'))
        self.assertEqual(vistor.count(), 2, "不相等")
