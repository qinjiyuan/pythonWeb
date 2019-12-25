#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import py_eureka_client.eureka_client as eureka_client
from tornado.options import define, options
import urllib

define("port", default=3333, help="run on the given port", type=int)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonWeb.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument('username', 'Hello')
        self.write(username + ', Administrator User!')


def init_eureka():
    print("开始注册到eureka！")
    tornado.options.parse_command_line()
    # 注册eureka服务
    eureka_client.init_registry_client(eureka_server="http://mixedinfos.top:8761/eureka/",
                                       app_name="register_client",
                                       # instance_host="在用一台机器的时候需要标记ip，否自会计算错误",
                                       instance_port=3333)
    # 获取eureka服务（有报错，先别用）
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
    init_eureka()
