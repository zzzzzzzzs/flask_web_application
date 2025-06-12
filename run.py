# -*- coding: utf-8 -*-
"""
启动文件
"""
from gevent import monkey
monkey.patch_all()

import os
from configs import config_obj

if __name__ == '__main__':
    # -------------------------Init File Folder-----------------------
    os.makedirs(config_obj['logger']['log_dir'], exist_ok=True)
    os.makedirs(
        os.path.join(
            config_obj['project']['temp_data_root'],
            config_obj['project']['avatar_path']
        ),
        exist_ok=True
    )

    from app import app
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer((app.host, app.port), app)
    http_server.serve_forever()
