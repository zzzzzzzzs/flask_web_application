# -*- coding: utf-8 -*-
"""
启动文件
"""
from app import app

if __name__ == '__main__':
    # print(app.url_map)
    app.run(host=app.host, port=app.port)
