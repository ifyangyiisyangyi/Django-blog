# -*- coding: utf-8 -*-
IMAGE_LIST = ['busybox', 'centos', 'docker', 'fedora', 'golang', 'httpd',
              'java', 'jenkins/jenkins', 'jenkinsci/blueocean', 'memcached',
              'mongo', 'mysql', 'nginx', 'node', 'php', 'postgres', 'python',
              'rabbitmq', 'redis', 'registry', 'ruby', 'tomcat', 'ubuntu', 'wordpress']

IZONE_TOOLS = {
    'office': {
        'tag': '办公工具',
        'tools': [
            {
                'name': '商品编码自动补齐',
                'url': 'tool:commdty_code_make_up',
                'img': 'editor/images/logos/regex.png',
                'desc': '自动补齐18位商品编码'
            },
            {
                'name': '计算分表',
                'url': 'tool:sub_table',
                'img': 'editor/images/logos/map.png',
                'desc': '根据会员编码计算分表'
            },
            {
                'name': 'mock',
                'url': 'tool:mock',
                'img': 'editor/images/logos/mock.png',
                'desc': '在线mock工具'
            },
            {
                'name': '常用链接',
                'url': 'tool:link_show',
                'img': 'editor/images/logos/link_show.png',
                'desc': '常用链接'
            },
            {
                'name': '获取天气',
                'url': 'tool:get_weather',
                'img': 'editor/images/logos/get_weather.png',
                'desc': '获取天气'
            },
            {
                'name': '爬虫',
                'url': 'tool:article_spider',
                'img': 'editor/images/logos/article_spider.png',
                'desc': '爬取python文章'
            },
            {
                'name':'md5加密',
                'url' : 'tool:md5',
                'img' : 'editor/images/logos/md5.png',
                'desc': 'md5加密'
            },
            {
                'name': 'base64加密',
                'url': 'tool:base64',
                'img': 'editor/images/logos/base64.png',
                'desc': 'base64加密'
            },
            {
                'name': 'job',
                'url': 'tool:job',
                'img': 'editor/images/logos/job.png',
                'desc': '招聘网站岗位信息'
            }
        ]
    }
}

if __name__ == '__main__':
    print(sorted(IMAGE_LIST))
