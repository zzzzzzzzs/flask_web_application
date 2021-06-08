"""
    Description:
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-07
    :python version: 3.5
"""
from functools import wraps
from flask import abort
from flask_login import current_user
from mongoengine import DoesNotExist
from model.user import Role
from utils import make_response_data
from utils.status_code import UserStatusCode


ADD_ADMIN = 'ADD_ADMIN'
DELETE_ADMIN = 'DELETE_ADMIN'
EDIT_ADMIN = 'EDIT_ADMIN'
QUERY_ALL_USER = 'QUERY_ALL_USER'
ADD_USER = 'ADD_USER'
DELETE_USER = 'DELETE_USER'
EDIT_USER = 'EDIT_USER'
ADD_PERMISSION = 'ADD_PERMISSION'
DELETE_PERMISSION = 'DELETE_PERMISSION'
QUERY_PERMISSION = 'QUERY_PERMISSION'
DISTRIBUTE_PERMISSION = 'DISTRIBUTE_PERMISSION'

SUPER_ADMIN = "超级管理员"
ADMIN = "管理员"
USER = "用户"

PERMISSIONS = [
    ("添加管理员", ADD_ADMIN, 2),
    ("删除管理员", DELETE_ADMIN, 2),
    ("编辑管理员信息", EDIT_ADMIN, 2),
    ("查看所有用户", QUERY_ALL_USER, 1),
    ("添加用户", ADD_USER, 1),
    ("删除用户", DELETE_USER, 1),
    ("编辑用户信息", EDIT_USER, 1),
    ("增加权限", ADD_PERMISSION, 2),
    ("删除权限", DELETE_PERMISSION, 2),
    ("查看所有权限", QUERY_PERMISSION, 1),
    ("分配权限", DISTRIBUTE_PERMISSION, 2)
]

ROLES = [(SUPER_ADMIN, 2), (ADMIN, 1)]


def _get_user_permission():
    """
    获取角色的所有权限
    :return: set
    """
    user_role_type = current_user.role_type
    try:
        role = Role.objects.get(role_type=user_role_type)
    except DoesNotExist:
        return set()
    return set(role.operation_permissions)


def auth(permission):
    def wrapper(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            permission_set = _get_user_permission()

            if permission not in permission_set:
                abort(403, make_response_data(**UserStatusCode.PERMISSION_NOT_ALLOW))

            return func(*args, **kwargs)

        return func_wrapper
    return wrapper