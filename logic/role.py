"""
    Description: 角色相关处理逻辑
    :author: zouzhisheng
    :copyright: (c) 2021, Tungee
    :date created: 2021-06-08
    :python version: 3.5
"""
import json
from flask import current_app
from utils import make_response_data
from utils.logger import log
from utils.status_code import BasicStatusCode
from configs import config_obj
from model.user import Role, Permission


def logic_get_roles_from_db():
    """
    从数据库获取角色信息
    :return: ok -> bool
             roles ->
    """
    try:
        roles = Role.objects.all()
        permissions = Permission.objects.only('name', 'action').filter(is_deleted=False)
    except Exception as e:
        log.logger.error(repr(e))
        return False, "数据库发生错误"

    # 重构permission数据结构
    new_permission = dict()
    for permission in permissions:
        name = permission.name
        action = permission.action
        new_permission[action] = name

    # 重构roles数据结构
    new_roles = list()
    for role in roles:
        new_operation = list()
        for action in role.operation_permissions:
            new_operation.append({
                'name': new_permission[action],
                'action': action
            })

        role.operation_permissions = new_operation
        new_roles.append(role.to_dict())

    return True, new_roles


def logic_filter_role_by_user(roles, user):
    """
    根据用户角色过滤roles列表
    :param roles:
    :param user:
    :return:
    """
    user_role_type = user.role_type
    if user_role_type == config_obj['ROLE']['SUPER_ADMIN']:
        # 如果是超级管理员，直接返回不过滤
        return roles

    # 比当前用户角色类型小的则添加进去
    new_roles = [role for role in roles if user_role_type > role.get('role_type', 0)]

    return new_roles


def logic_get_roles(user):
    """
    根据用户角色获取他可以看到的角色列表
    :return: ok->bool, status_code->int, msg
    """
    key = 'roles'
    redis_db = current_app.extensions['redis']

    # 从缓存获取角色信息，取出来是byte类型，需要转换
    roles = redis_db.get(key)

    # 如果缓存没有则从数据库获取
    if not roles:
        ok, roles = logic_get_roles_from_db()

        if not ok:
            return False, 500, make_response_data(**BasicStatusCode.DATABASE_ERROR)
        # 从数据库获取后存入缓存，并设置过期时间
        redis_db.set(key, json.dumps(roles), ex=config_obj['REDIS']['ROLE_EX'])
    else:
        roles = json.loads(roles)

    # 根据当前用户角色过滤可选的角色列表
    roles = logic_filter_role_by_user(roles, user)
    # 默认添加用户的角色
    roles.append({
        "name": "用户",
        "role_type": 0,
        "operation_permissions": []
    })
    return True, 200, make_response_data(roles)
