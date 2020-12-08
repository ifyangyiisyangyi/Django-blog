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
                'name': '计算分库分表',
                'url': 'tool:sub_table',
                'img': 'editor/images/logos/sub_tablel.png',
                'desc': '计算分库分表'
            }
        ]
    }
}

if __name__ == '__main__':
    print(sorted(IMAGE_LIST))
