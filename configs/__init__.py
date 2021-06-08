"""
初始化配置对象
"""
import os
import yaml

yaml_f = open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs.example.yaml'),
    'r', encoding='utf8'
)

config_obj = yaml.safe_load(yaml_f)
