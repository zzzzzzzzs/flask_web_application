"""
    Description:
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-04
    :python version: 3.5
"""
import os
import logging
from logging import handlers
from configs import config_obj


class Logger(object):
    def __init__(self, filename=None, level=None, max_bytes=102400,
                 backup_count=20, fmt=None):
        filename = config_obj['logger']['log_dir'] + '/' + filename
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level)

        formatter = logging.Formatter(fmt)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = handlers.RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

os.makedirs(config_obj['logger']['log_dir'], exist_ok=True)
os.makedirs(
    os.path.join(
        config_obj['project']['temp_data_root'],
        config_obj['project']['avatar_path']
    ),
    exist_ok=True
)


level = logging.DEBUG if bool(config_obj['APP']['DEBUG']) else logging.INFO
log = Logger(
    filename=config_obj['logger']['log_filename'],
    level=level,
    fmt=config_obj['logger']['format']
)