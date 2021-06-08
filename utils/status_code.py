"""
    Description:
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-05
    :python version: 3.5
"""


class BasicStatusCode(object):
    SERVER_ERROR = {
        'code': 1001,
        'message': "服务器发生了未知错误"
    }
    DATABASE_ERROR = {
        'code': 1002,
        'message': '数据库发生了未知错误'
    }
    INVALID_ARGS = {
        'code': 1003,
        'message': '非法参数'
    }
    TIMEOUT_ERROR = {
        'code': 1004,
        'message': '超时错误'
    }


# 用户模块返回状态码及信息
class UserStatusCode(BasicStatusCode):
    PASSWORD_ERROR = {
        'code': 2001
    }
    EXISTED_ERROR = {
        'code': 2002
    }
    NOT_EXIST_ERROR = {
        'code': 2003
    }
    WRONG_PWD_OR_ACCOUNT = {
        'code': 2004,
        'message': '用户名或密码错误'
    }
    INVALID_USER_ID = {
        'code': 2005,
        'message': '非法的user_id'
    }
    PERMISSION_NOT_ALLOW = {
        'code': 2006,
        'message': '权限不允许'
    }